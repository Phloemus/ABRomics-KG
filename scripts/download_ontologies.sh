
DIR="../ontologies"
FILENAME="aro.owl"

FILE_PATH="$DIR/$FILENAME"

if [ -f "$FILE_PATH" ]; then
    echo "File '$FILENAME' already exists in '$DIR'."
    
    read -p "Do you want to delete this file? (y/n): " CONFIRM

    if [ "$CONFIRM" = "y" ] || [ "$CONFIRM" = "Y" ]; then
        rm "$FILE_PATH"
        wget https://raw.githubusercontent.com/arpcard/aro/master/aro.owl -O $FILE_PATH
        echo "New file replaced in '$FILE_PATH'"
    else
        echo "Operation cancelled. File not deleted."
    fi
else
    wget https://raw.githubusercontent.com/arpcard/aro/master/aro.owl -O $FILE_PATH
    echo "New file replaced in '$FILE_PATH'"
fi

