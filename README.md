# CSCE_310_Project

conda commands 
## Exports your environment
conda env export > environment.yml 

## Creat environment from file 
conda env create -f environment.yml

# Update environment from File 
conda activate csce310
conda env update --file environment.yml --prune

## Alembic 

- Alembic creates databases from python classes
- After you write code in models.py, you run `alembic revision --autogenerate -m "comments"`
- Then this creates the a file under alembic/versions
- Finally, when you run `alembic upgrade head` this will execute the changes you made and edit the Database 

