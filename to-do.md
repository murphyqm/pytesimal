# To-Do

- Sort out plotting module - migrate and merge simple plotting module from module output data rep and combine
- Set up Jupyter Notebook example that runs model and plots result. Need to build plotting in so it can be called without saving arrays (current, messy version does this but need cleaner version to work too)
- Function naming and documentation - need to clean and make sure is useful and up to date
- Allow T-dep function to be customized and included as argument?

## Worklog/notes

### 9th Nov

Want to allow the user to specify the output folder, instead of just a folder name.
Will need to be updated across all modules - but can avoid tricky issues with relative path names etc by requiring an absolute path name to be input at beginning.
This also won't change the interface too much - except that absolute paths will need to be provided instead of just a folder name.
Will maintain an outputs folder still for testing purposes - need to decide how that will work/what will still save there.
Will need to think about how this will affect tests... and elsewhere where foldername is req'd...

Also want to look into parellelising Travis.ci testing: https://docs.travis-ci.com/user/speeding-up-the-build/

- Going for it - removing "output_runs" from file path (except testing scripts)
- Tests are passing - seems to work well! Now to figure out how to load from outside the directory, so scripts don't need to be run inside "planetesimal-cooling"
- ok. So potential issue: have used a hyphen in the repository name... which is a bit of an issue! This raises a python syntax error, as hyphens are not allowed in module or package names. Oops!
- This then additionally raises issues with all subsequent imports - they're relative... how to easily fix? Need to redo these anyway because the modules need to be shifted around a bit and file structure thought about.

Could just temporarily change the working path:

```
import os

os.chdir("**Put here the directory where you have the file with your function**")

from file import function

os.chdir("**Put here the directory where you were working**")
```

This could work for now?

- the above workaround works for now, but need to think about renaming github repository which is a bit of a pain.