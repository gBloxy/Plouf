# Plouf

Plouf is a simple tool for sending custom http requests implemented in python.  
Ploof currently support 7 request methods : GET, POST, HEAD, PUT, DELETE, PATCH, and OPTIONS. 
This tool is not professional and only meant for testing and CTFs.  
It does not work with other network protocols.

## Screenshots

![Capture](https://github.com/gBloxy/Plouf/assets/121670440/70e7120a-f952-4d84-8077-ff894dc3e42e)

## Usage

To start the application, run the `plouf.py` python file.  
To make a request, first choose the targeted url, select the request method with the drop down menu, then custom the headers, and finally click the Send button.  
Use the data box input to send data to the server in case of a POST, PUSH, or PATCH request.

## Requirements

* Make sure you have python installed.  
* Use the package manager [pip](https://pip.pypa.io/en/stable/) to install [PyQt5](https://riverbankcomputing.com/software/pyqt/).  
```bash
pip install PyQt5
```

## Contributing

If you encounter any issues, have suggestions, or need support, please don't hesitate to reach out by creating an issue in the repository.  
All feedbacks are welcome.

## License

Plouf is licensed under the MIT license. See the `LICENSE` file for details.
