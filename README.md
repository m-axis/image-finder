# image-finder
Image finder is a tool which helps find all the duplicate images in your machine and show a preview of the duplicate images in HTML format. The tool will also be able to filter the duplicate images out and place them in separate directory.

## Execution command
```console
python cleanUp.py your/folder/path ["your", "file", "extensions", "to", "check"]
```

### To find the duplicates in specified folder and file extensions
```console
python cleanUp.py C:/ ["png", "jpg", "ico", "jpeg", "tif", "gif"]
```

### To find the duplicates in the current folder and default file extensions
```console
python cleanUp.py
```


