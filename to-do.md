# To-Do

- Sort out plotting module - migrate and merge simple plotting module from module output data rep and combine
- Set up Jupyter Notebook example that runs model and plots result. Need to build plotting in so it can be called without saving arrays (current, messy version does this but need cleaner version to work too)
- Function naming and documentation - need to clean and make sure is useful and up to date
- Allow T-dep function to be customized and included as argument?

# Worklog/notes 

## 9th Nov

Want to allow the user to specify the output folder, instead of just a folder name. Will need to be updated across all modules - but can avoid tricky issues with relative path names etc by requiring an absolute path name to be input at beginning. This also won't change the interface too much - except that absolute paths will need to be provided instead of just a folder name. Will maintain an outputs folder still for testing purposes - need to decide how that will work/what will still save there.
