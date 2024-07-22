import sympy as sp

from ml_modules.inference import classifier
from settings import INTEGRATION_VARIABLE_NAME

if __name__ == "__main__":
    while True:
        text = input("Enter an integrand: ")
        result = classifier(f"Is {text} integrable?")
        print(f"Prediction: {result[0]['label']}")
        print(f"Score: {result[0]['score']}")
        integral = sp.integrate(
            text, sp.symbols(INTEGRATION_VARIABLE_NAME)
        )
        print(f"Integral: {integral}")
