class Prompter:
    def __init__(self):
        self.templates = {
            "default":[
                {"role": "system", "content": "{system}"},
                {"role": "user", "content": "{instruction}"},
                {"role": "assistant", "content": "{output}"}
            ],
            "no_system_prompt":[
                {"role": "user", "content": "{instruction}"},
                {"role": "assistant", "content": "{output}"}
            ]
        }

    def prompt_generator(self, tokenizer, use_system_prompt):
        if tokenizer.chat_template is None:
            tokenizer.chat_template = (
                "{% for message in messages %}"
                "{% if loop.first and messages[0]['role'] != 'system' %}"
                "{{ '### system\nYou are a helpful assistant.\n\n' }}"
                "{% endif %}"
                "{{'### ' + message['role'] + '\n' + message['content'] + '\n\n'}}"
                "{% endfor %}"
                "{% if add_generation_prompt %}{{ 'assistant\n' }}{% endif %}"
            )

        template = self.templates['no_system_prompt'] if use_system_prompt is False else self.templates['default']
        prompt = tokenizer.apply_chat_template(template, tokenize=False)
        prompt += tokenizer.eos_token if not prompt.endswith(tokenizer.eos_token) else ""

        prompt = prompt.split("{output}")

        return prompt[0], "{output}"+prompt[1]