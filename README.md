# All in AI Demo App
A demo app for the [All in AI](https://allinevent.ai/) presentation on September 27, 2023.

Presented by Nathan Drezner ([@ndrezn](https://github.com/ndrezn)).

This application uses [Dash Chart Editor](https://github.com/BSd3v/dash-chart-editor) and the [OpenAI Python library](https://github.com/openai/openai-python) to build an application allowing users to ask questions about a dataset and persist views of their dataset with analytics associated.

## Usage
> Note: You must provide an [OpenAI API key](https://platform.openai.com/account/api-keys) as an environment variable at `$OPEN_AI_KEY`.

Install the dependencies with:
```
pip install -r requirements.txt
```

And run the application with:
```
python app.py
```

Or, provide your API key directly if it is not in your environment:
```
OPEN_AI_KEY=... python app.py
```
