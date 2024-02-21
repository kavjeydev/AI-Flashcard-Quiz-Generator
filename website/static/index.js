function deleteNote(noteId){
    fetch('/delete-note', {
        method: 'POST',
        body: JSON.stringify({ noteId: noteId}),
    }).then((_res) => {
        window.location.href="/";
    });
}

function deleteCard(flashID){
    fetch('/delete-card', {
        method: 'POST',
        body: JSON.stringify({ flashID: flashID}),
    }).then((_res) => {
        window.location.href="/flashcards";
    });
}

function deleteGroup(groupID){
    fetch('/delete-group', {
        method: 'POST',
        body: JSON.stringify({ groupID: groupID}),
    }).then((_res) => {
        window.location.href="/groups";
    });
}