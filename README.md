# CV / Cover Letter Creator Reborn

Automation of CV / cover letter creation via jobs from www.seek.co.nz.

# Installation
`pip install requirements.txt`

# Usage
`python app.py`

## Setting up your documents

### Placeholders

Placeholders are special pieces of text which the Creator can replace with the job values. For example, if we were applying to a job that was:
* Listed by ACME Products 123
* Called Senior Snack Eater
* Located in Antarctica

then our template like this...

```
Dear COMPANY_NAME,

I am writing today to express my interest in the JOB_TITLE position in LOCATION_NAME, as advertised on www.seek.co.nz.
```

might become...

```
Dear ACME Products 123,

I am writing today to express my interest in the Senior Snack Eater position in Antarctica, as advertised on www.seek.co.nz.
```

The tags that can be used are:
| Tag Name | Description | Example |
|----------|-------------|---------|
| JOB_TITLE | The title of the job position being applied for | "Senior AI Engineer" |
| COMPANY_NAME | The name of the company offering the position | "Tech Innovations Inc." |
| LOCATION_NAME | The geographic location of the job opportunity | "London, UK" |
| DATE | The current date when the application is being prepared | "15/01/2024" |

### ChatGPT Integration
1. Sign up for a developer's account at [OpenAI developer platform](https://platform.openai.com).
2. Create an API key.
3. Add a small amount of credit to the account. ($5 is more than enough.)
4. Create a `./.env` file in this project.
5. Copy the API key and add it to a `OPENAI_KEY` value in the .env file.
```
# .env
OPENAI_KEY=sk-proj-ThiS-iS-A_fakE-key
```
6. Add ChatGPT tags to your documents in this format: `<CHAT_GPT>QUERY</CHAT_GPT>`. For example:
```
# the job description will be automatically added after your prompt

<CHAT_GPT>In two sentences, write about why this job would provide good learning opportunities. Write this in the first-person perspective of a potential candidate talking to their future boss.</CHAT_GPT>
```

## Prefilled GUI Values

You can make your own GUI creation script with prefilled GUI values by using the CreatorGUI class. This means that you won't have to fill in the template path / output dir values every time you open the GUI.
```
# './scripts/my_gui.py'

from requests_cache import CachedSession

from cv_creator_reborn.app import CreatorGUI, tk

root = tk.Tk()
session = CachedSession('seek_cache', 'sqlite')
app = CreatorGUI(
    root,
    name="Your Name Here",
    template_path="/path/to/my/cover_letter_template.docx",
    output_dir="/path/to/my/outputs_dir",
    session=session
)
app.root.mainloop()
```

## File Type Interpolation
When using the CreatorGUI, any template you provide will be automatically checked for 'cv' or 'cover_letter' in the beginning of its name. If none is found, the template will be assumed to be a cover letter. This is used in correctly naming the output file.
