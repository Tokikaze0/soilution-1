import os
import numpy as np
import joblib
import tensorflow as tf
from django.conf import settings

class CropService:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.encoder = None
        self.model_path = os.path.join(settings.BASE_DIR, 'detector', 'ml_models', 'crop_recommendation_model_v3.keras')
        self.scaler_path = os.path.join(settings.BASE_DIR, 'detector', 'ml_models', 'scaler.pkl')
        self.encoder_path = os.path.join(settings.BASE_DIR, 'detector', 'ml_models', 'encoder.pkl')
        self._load_resources()

    def _load_resources(self):
        """Load model and preprocessors if they exist."""
        try:
            if os.path.exists(self.model_path):
                self.model = tf.keras.models.load_model(self.model_path)
                print("Keras model loaded successfully.")
            else:
                print(f"Model file not found at {self.model_path}")

            if os.path.exists(self.scaler_path):
                self.scaler = joblib.load(self.scaler_path)
                print("Scaler loaded successfully.")
            else:
                print(f"Scaler file not found at {self.scaler_path}")

            if os.path.exists(self.encoder_path):
                self.encoder = joblib.load(self.encoder_path)
                print("Encoder loaded successfully.")
            else:
                print(f"Encoder file not found at {self.encoder_path}")

        except Exception as e:
            print(f"Error loading ML resources: {e}")

    def get_crop_recommendations(self, nitrogen, phosphorus, potassium, temperature, humidity, ph):
        """
        Predict crop recommendations based on soil parameters.
        Returns a list of dictionaries with crop name and confidence.
        
        Model expects 6 features: N, P, K, Temperature, Humidity, pH
        """
        if not all([self.model, self.scaler, self.encoder]):
            return [{"name": "Error", "confidence": 0, "message": "ML resources not loaded"}]

        try:
            # Prepare input array in the EXACT order the model was trained
            # Order: N, P, K, Temperature, Humidity, pH (6 features)
            input_data = np.array([[nitrogen, phosphorus, potassium, temperature, humidity, ph]])
            
            # Scale the features
            input_scaled = self.scaler.transform(input_data)
            
            # Predict
            prediction_probs = self.model.predict(input_scaled)
            
            # Get all predictions sorted by confidence
            all_indices = np.argsort(prediction_probs[0])[::-1]
            
            recommendations = []
            for idx in all_indices:
                confidence = float(prediction_probs[0][idx]) * 100
                
                if confidence > 0:
                    # Get crop name from encoder
                    if hasattr(self.encoder, 'categories_'):
                        crop_name = self.encoder.categories_[0][idx]
                    elif hasattr(self.encoder, 'classes_'):
                        crop_name = self.encoder.classes_[idx]
                    else:
                        crop_name = f"Crop {idx}"

                    recommendations.append({
                        "name": crop_name,
                        "confidence": round(confidence, 2)
                    })
            
            # Return top 5 recommendations
            return recommendations[:5]

        except Exception as e:
            print(f"Prediction error: {e}")
            return [{"name": "Error", "confidence": 0, "message": str(e)}]

class SoilService:
    def analyze_soil(self, nitrogen, phosphorus, potassium, temperature, humidity, ph):
        """
        Analyze soil health based on parameters.
        Updated to use humidity instead of moisture and removed conductivity.
        """
        status = "Healthy"
        issues = []

        # Nitrogen analysis
        if nitrogen < 20:
            issues.append("Low Nitrogen - Consider nitrogen-rich fertilizers")
        elif nitrogen > 100:
            issues.append("High Nitrogen - May cause excessive vegetative growth")

        # Phosphorus analysis
        if phosphorus < 20:
            issues.append("Low Phosphorus - Add phosphate fertilizers")
        elif phosphorus > 80:
            issues.append("High Phosphorus - May inhibit micronutrient uptake")
        
        # Potassium analysis
        if potassium < 20:
            issues.append("Low Potassium - Add potash fertilizers")
        elif potassium > 80:
            issues.append("High Potassium")

        # pH analysis
        if ph < 5.5:
            issues.append("Acidic Soil (pH < 5.5) - Consider liming")
        elif ph > 7.5:
            issues.append("Alkaline Soil (pH > 7.5) - May limit nutrient availability")

        # Humidity analysis
        if humidity < 40:
            issues.append("Low Humidity - May stress plants")
        elif humidity > 85:
            issues.append("High Humidity - Risk of fungal diseases")

        # Temperature analysis
        if temperature < 15:
            issues.append("Low Temperature - May slow plant growth")
        elif temperature > 35:
            issues.append("High Temperature - May stress plants")

        if issues:
            status = "Needs Attention"

        details = f"Soil is {status.lower()}."
        if issues:
            details += " " + " ".join(issues) + "."

        return {
            "status": status,
            "issues": issues,
            "details": details
        }

# Create singleton instances
crop_service = CropService()
soil_service = SoilService()