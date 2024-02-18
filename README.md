## Prerequisites

**Python**

Various `conda` invocations to manage a python environment:

```bash
conda env list
conda create --name py4ai
conda install python=3.9
conda activate py4ai
conda deactivate
```

**CS50 tools**

- [Installing check50](https://cs50.readthedocs.io/projects/check50/en/latest/index.html)

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
