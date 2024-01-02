# Read me

## General info
This project allows you to sort/group photos on your Dropbox account and then remove duplicate ones

## Configuration
Create `config.json` file
```cp config.template.json config.json```

```json
{
    "dropbox": {
        "api_token": "YOUR_DROPBOX_API_TOKEN"
    },
    "store": { // config for option 1
        "target_dir": "/photos",
        "source_dirs": [
            "/source-dir1",
            "/source-dir2"
        ]
    },
    "group": { // config for option 2
        "directory": "/photos"
    },
    "duplicates": { // config for option 3
        "directories_to_find": [
            "/photos"
        ]
    },
    "directories": { // config for option 5
        "to_maintain": [
            "/photos/travels",
            "/photos/child"
        ],
        "to_remove": [
            "/photos/camera"
        ]
    },
    "exclude": { // config for option 6
        "base_dir": "/photos",
        "temporary_trash_dir": "/photos-trash"
    }
}
```

## Available options
1. Move source files from input directories to destination folder
2. Generate directory tree structure `./yyyy/mm` and move there files by create date
3. Get duplicated photos and store them in `duplicates_by_hash.json`
4. Get unique directories to identify original files and duplicates manually
5. Resolve filenames for original files and duplicates
6. Move duplicates to external folder (then you can remove them manually if you are sure that you really do not need them)