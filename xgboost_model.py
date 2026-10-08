import numpy as np

from xgboost import XGBRegressor

from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    r2_score,
    mean_squared_error,
    mean_absolute_error
)


class XGBoostModel:

    FEATURES = [
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
        "RSI",
        "SMA_7",
        "SMA_20",
        "Volume_Ratio"
    ]

    def __init__(self):
        self.model = XGBRegressor(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.05,
            random_state=42
        )

        self.x_scaler = StandardScaler()
        self.y_scaler = StandardScaler()

    def train(self, data):

        X = data[self.FEATURES]
        y = data["Close"].shift(-1)

        # Remove final row because next-day target doesn't exist
        X = X.iloc[:-1]
        y = y.iloc[:-1]

        # Chronological 80/20 split
        split_index = int(len(X) * 0.8)

        X_train = X.iloc[:split_index]
        X_test = X.iloc[split_index:]

        y_train = y.iloc[:split_index]
        y_test = y.iloc[split_index:]

        # Scale features
        X_train_scaled = self.x_scaler.fit_transform(X_train)
        X_test_scaled = self.x_scaler.transform(X_test)

        # Scale target
        y_train_scaled = self.y_scaler.fit_transform(
            y_train.values.reshape(-1, 1)
        ).ravel()

        # Train
        self.model.fit(
            X_train_scaled,
            y_train_scaled
        )

        # Predict
        predictions_scaled = self.model.predict(
            X_test_scaled
        )

        predictions = self.y_scaler.inverse_transform(
            predictions_scaled.reshape(-1, 1)
        ).ravel()

        # Metrics
        r2 = r2_score(y_test, predictions)

        rmse = np.sqrt(
            mean_squared_error(
                y_test,
                predictions
            )
        )

        mae = mean_absolute_error(
            y_test,
            predictions
        )

        # Directional accuracy
        actual_direction = np.sign(
            y_test.values -
            X_test["Close"].values
        )

        predicted_direction = np.sign(
            predictions -
            X_test["Close"].values
        )

        directional_accuracy = (
            actual_direction ==
            predicted_direction
        ).mean() * 100

        metrics = {
            "R2 Score": r2,
            "RMSE": rmse,
            "MAE": mae,
            "Directional Accuracy":
                directional_accuracy
        }

        return metrics

    def predict_next_day(self, data):

        latest = data[self.FEATURES].iloc[-1:]

        latest_scaled = self.x_scaler.transform(
            latest
        )

        prediction_scaled = self.model.predict(
            latest_scaled
        )

        prediction = self.y_scaler.inverse_transform(
            prediction_scaled.reshape(-1, 1)
        )

        return float(prediction[0][0])
