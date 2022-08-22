// this function takes an argument(noteId), sends a post request to the backend(endpoint) -> delete-note 
// route in views.py, then reloads/refreshes the window after getting a response

function deleteNote(noteId){
    fetch('/delete-note', {
        method: 'POST',
        body: JSON.stringify({ noteId: noteId})// this converts noteId to a string
    }).then((_res ) => {
        window.location.href = '/notes';
    });
}