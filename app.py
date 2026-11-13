
import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
from streamlit_drawable_canvas import st_canvas

# Page configuration
st.set_page_config(
    page_title="MNIST Digit Recognition",
    page_icon="🔢",
    layout="centered"
)

st.title("🔢 Handwritten Digit Recognition")
st.write("Draw a digit from 0 to 9 and let AI recognize it.")

# Load trained model
@st.cache_resource
def load_model():
    return tf.keras.models.load_model("mnist_digit_model.keras")

model = load_model()

# Drawing canvas
canvas_result = st_canvas(
    fill_color="rgba(0, 0, 0, 0)",
    stroke_width=18,
    stroke_color="#FFFFFF",
    background_color="#000000",
    height=280,
    width=280,
    drawing_mode="freedraw",
    key="canvas",
    return_image_data=True
)

# Prediction button
if st.button("Predict Digit", type="primary"):

    if canvas_result.image_data is None:
        st.warning("Please draw a digit first.")

    else:
        # Convert canvas to grayscale
        image = Image.fromarray(
            canvas_result.image_data.astype("uint8")
        ).convert("L")

        image_array = np.array(image)

        # Find digit pixels
        coords = np.argwhere(image_array > 30)

        if len(coords) == 0:
            st.warning("Please draw a digit first.")

        else:
            # Crop around the digit
            y_min, x_min = coords.min(axis=0)
            y_max, x_max = coords.max(axis=0)

            cropped = image_array[
                y_min:y_max + 1,
                x_min:x_max + 1
            ]

            # Resize while maintaining aspect ratio
            digit = Image.fromarray(cropped)
            digit.thumbnail(
                (20, 20),
                Image.Resampling.LANCZOS
            )

            # Create 28x28 black image
            mnist_image = Image.new(
                "L", (28, 28), 0
            )

            # Center digit
            x_offset = (28 - digit.width) // 2
            y_offset = (28 - digit.height) // 2

            mnist_image.paste(
                digit,
                (x_offset, y_offset)
            )

            # Normalize pixels
            processed = (
                np.array(mnist_image).astype("float32") / 255.0
            )

            # Model prediction
            prediction = model.predict(
                processed.reshape(1, 28, 28),
                verbose=0
            )

            predicted_digit = int(
                np.argmax(prediction)
            )

            confidence = float(
                np.max(prediction)
            ) * 100

            # Display results
            st.image(
                mnist_image,
                caption="Processed 28x28 MNIST image",
                width=200
            )

            st.success(
                f"Predicted Digit: {predicted_digit}"
            )

            st.metric(
                "Prediction Probability",
                f"{confidence:.2f}%"
            )

            # Display all digit probabilities
            st.write("### Prediction probabilities")

            st.bar_chart(
                prediction[0],
                x_label="Digit",
                y_label="Probability"
            )
