# CS50 AI with Python submissions

These are my submissions for CS50's [Introduction to Artificial Intelligence with Python](https://pll.harvard.edu/course/cs50s-introduction-artificial-intelligence-python) course.

The CS50 course has exercises which must be completed in Python, and a number of tools for checking and submitting code to be automatically assessed.

## Prerequisites

There are a number of tools required. Details below are for OS X.

**Python**

I'm using [Anaconda Python](https://www.anaconda.com/).

You can either install Anaconda by download, or through Homebrew:

```bash
brew install --cask anaconda
```

You may also have to update your `.zshrc` paths:

```bash
echo 'export PATH=/usr/local/anaconda3/bin:$PATH' >> ~/.zshrc
echo 'export PATH=/opt/homebrew/anaconda3/bin:$PATH' >> ~/.zshrc
source ~/.zhsrc
```

There are various `conda` invocations to manage Python environments, which mean you can control the version of python and the packages available for each project that you work on...

```bash
conda env list
conda create --name py4ai
conda install python=3.9
conda activate py4ai
conda deactivate
```

**CS50 tools**

The various CS50 tools can be installed through `pip`. See: [Installing check50](https://cs50.readthedocs.io/projects/check50/en/latest/index.html)

```bash
pip install check50
pip install style50
pip install submit50
```

`style50` has a dependency on libmagic:

```bash
brew install libmagic
```

## Invocations

Enter the project root directly. Test and submit with the appropriate slug.

| Project               | Directory   | Slug                             |
| --------------------- | ----------- | -------------------------------- |
| Degrees of separation | `degrees`   | `ai50/projects/2024/x/degrees`   |
| Tic-Tac-Toe           | `tictactoe` | `ai50/projects/2024/x/tictactoe` |

```bash
check50 <slug>
style50 <slug>
submit50 <slug>
```
