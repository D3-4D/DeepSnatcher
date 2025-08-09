# DeepSnatcher

DeepSnatcher is a reverse-engineered API key snatcher designed to interact with the free DeepAI models. It replicates the TryIt API key generation mechanism to facilitate requests to DeepAI's endpoints, enabling enhanced control and experimentation with their AI services.

Credit is due to @5eero for developing a similar module earlier. DeepSnatcher was built independently without any resource of his project. This project is developed and maintained by @D3-4D.

## Features

- Session-based API client with history tracking and request indexing.
- Supports all free models (`standard`, `online`, `math`).
- Streaming or non-streaming response handling.
- API key generator for request authentication.
- Basic logging support.

## Installation

Ensure you have Python 3.7 or higher installed. Then, install the required dependencies using pip and the provided `requirements.txt` file:

```bash
pip install -r requirements.txt
