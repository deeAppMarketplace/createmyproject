# Jules API Interface

This project provides a simple web interface to interact with the Jules API. It allows users to dynamically provide information about a GitHub organization, repository, prompt, branch, and title to initiate a Jules session.

## Features

-   **User-friendly web interface:** A clean and simple form to input the necessary parameters for the Jules API.
-   **Dynamic API calls:** Constructs and sends requests to the Jules API based on user input.
-   **Secure API key handling:** Uses environment variables to manage the Jules API key, ensuring it's not hard-coded in the source.
-   **Ready for deployment:** Includes a `render.yaml` file for easy deployment on the Render platform.
-   **Comprehensive documentation:** Sphinx-generated documentation for the project's codebase.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/jules-api-interface.git
    cd jules-api-interface
    ```

2.  **Create a virtual environment and activate it:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set the JULES_API_KEY environment variable:**
    ```bash
    export JULES_API_KEY='your_jules_api_key'
    ```

## Usage

1.  **Run the Flask application:**
    ```bash
    python app.py
    ```

2.  **Open your web browser** and navigate to `http://127.0.0.1:5000`.

3.  **Fill out the form** with the required information:
    -   GitHub Organization
    -   GitHub Repository
    -   Starting Branch
    -   Title
    -   Prompt

4.  **Click "Submit"** to send the request to the Jules API. The response will be displayed on the page.

## Deployment on Render

This application is configured for deployment on Render.

1.  **Fork this repository** to your GitHub account.

2.  **Create a new "Web Service"** on Render and connect it to your forked repository.

3.  Render will automatically detect the `render.yaml` file and configure the service.

4.  **Add a secret file** or environment variable for `JULES_API_KEY` in the Render dashboard.
    -   **Key:** `JULES_API_KEY`
    -   **Value:** Your Jules API key

5.  **Deploy the service.** Render will build and deploy the application. Once the deployment is complete, you can access the application at the URL provided by Render.

## Documentation

The documentation for this project is generated using Sphinx. To build the documentation locally, follow these steps:

1.  **Install Sphinx:**
    ```bash
    pip install sphinx
    ```

2.  **Navigate to the `docs` directory:**
    ```bash
    cd docs
    ```

3.  **Build the HTML documentation:**
    ```bash
    make html
    ```

4.  **Open the generated documentation** in your browser at `docs/_build/html/index.html`.

## Local development conveniences

You can keep a local `.env` file (already git-ignored) with development secrets. Example `.env`:

```
JULES_API_KEY=your_jules_api_key_here
```

The application will automatically load `.env` in local development if `python-dotenv` is installed. Alternatively you can export the variable manually:

```bash
export JULES_API_KEY='your_jules_api_key'
```

## Running tests

Run the pytest suite (the tests mock external network calls):

```bash
source venv/bin/activate
pip install -r requirements.txt
pytest -q
```

## Git hooks (prevent committing .env)

This repository includes a simple pre-commit hook in `.githooks/pre-commit` that prevents accidentally committing a `.env` file.

Enable it locally with:

```bash
git config core.hooksPath .githooks
```

After running that command, the pre-commit hook will run automatically when committing.

