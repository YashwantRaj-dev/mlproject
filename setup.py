from setuptools import find_packages, setup # type: ignore

def get_requierements(file_path:str)->list[str]:
    # this function will return the list of requirements
    requierements = []
    with open(file_path) as file_obj:
        requierements = file_obj.readlines()
        requierements = [req.replace("\n","") for req in requierements]
        
        if "-e ." in requierements:
            requierements.remove("-e .")
    return requierements

setup(
    name="mlproject",
    version="0.1.0",
    author="Yashwant",
    author_email="yr15112003@gmail.com",
    packages=find_packages(),
    install_requires=get_requierements('requirements.txt')   
)
