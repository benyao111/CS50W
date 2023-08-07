document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  document.querySelector('#compose-form').addEventListener('submit', event => {
    event.preventDefault() //prevents form submission
    fetch('/emails', {
        method: 'POST',
        body: JSON.stringify({
            recipients: document.querySelector('#compose-recipients').value,
            subject: document.querySelector('#compose-subject').value,
            body: document.querySelector('#compose-body').value
            })
        })
        .then(response => response.json())
        .then(() => {

            load_mailbox('sent');
        });
        return false;
    });

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  //document.querySelector('#container2').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  //sending email moved above because otherwise every time we press compose email we add a new event handler so you end up submitting multiple mails
  };


function load_mailbox(mailbox) {


  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  //document.querySelector('#container2').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  //load the mails for inbox
  //if (mailbox == 'inbox') {
      fetch(`/emails/${mailbox}`)
      .then(response => response.json())
      .then(emails => {
        emails.forEach((i) => { //issue MUST be here i think. for some reason, the same email shows multiple times on sent inbox
            const element = document.createElement('div');
            element.id = `email_${i['id']}`;
            element.style.cssText = 'margin: 15px; padding: 15px; border: solid black 2px; border-radius: 10px; cursor:pointer;';
            element.innerHTML = `
                <div class = 'row'>
                    <div class = 'col-md-2'>From: </div>
                    <div class = 'col-md-7'>Subject:</div>
                    <div class = 'col-md-3'>Timestamp:</div>
                </div>
                <div class = 'row'>
                    <div class = 'col-md-2'>${i['sender']} </div>
                    <div class = 'col-md-7'>${i['subject']} </div>
                    <div class = 'col-md-3'>${i['timestamp']} </div>
                </div>
                `;
            //click = read
            element.addEventListener('click', function() {
                fetch(`emails/${i['id']}`, {
                method: "PUT",
                body: JSON.stringify({
                    read: true
                    })
                    });
                element.style.cssText = 'margin: 15px; padding: 15px; border: solid black 2px; border-radius: 10px; cursor:pointer; background-color: gray';
                load_mail(i['id'])
                //after page refresh this doesnt work
            })
            //set read to gray
            if (i['read'] == true) {
                element.style.cssText = 'margin: 15px; padding: 15px; border: solid black 2px; border-radius: 10px; cursor:pointer; background-color: gray';
                }

            //if (emails[i]['recipients'].includes(document.querySelector('h2'))) {

            document.querySelector('#emails-view').append(element);
            //if i append to a new view like "container2" everything becomes strange.
            //emails-view seems set up so that things will be deleted after calling once
            //(no multiple fetch requests that appear after clicking inbox twice and i dont need to specify inbox, sent, etc)
            //The reason is line 56 clears the div (emails-views) to just say the inbox name every time you click inbox, sent, etc
      })})
//}
}

function load_mail(email_id) {
    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    //document.querySelector('#container2').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'block';

    //fetch email details

    fetch(`/emails/${email_id}`)
    .then(response => response.json())
    .then(email => {
    // Print email
        element = document.querySelector('#email-view')
        element.innerHTML = `
            <div> <strong> From: </strong> ${email['sender']} </div>
            <div> <strong>To: </strong> ${email['recipients']} </div>
            <div> <strong> Subject: </strong> ${email['subject']}</div>
            <div> <strong> Timestamp: </strong> ${email['timestamp']}</div>
            <button class = 'btn btn-sm btn-outline-primary' id = 'unreadbtn'> Mark as Unread </button>
        `
        element.innerHTML += !email['archived'] ? `<button class = 'btn btn-sm btn-outline-primary' id = 'archivebtn'> Archive </button>` :
        `<button class = 'btn btn-sm btn-outline-primary' id = 'archivebtn'> Unarchive </button>`

        element.innerHTML +=
        `
            <button class = 'btn btn-sm btn-outline-primary' id = 'replybtn'> Reply </button>
            <hr>
            <div> ${email['body']} </div>
        `

        //add event listener for archive, still have to figure out how to make it so that send and archive mailboxes differ
        document.querySelector('#archivebtn').addEventListener('click', function() {
        fetch(`/emails/${email_id}`, {
        method: "PUT",
        body: JSON.stringify({
            archived: !email['archived'] //changes to opposite when clicked
        })
        })
        .then(() => {load_mailbox('inbox')})
        })
        //reply button listener
        document.querySelector('#replybtn').addEventListener('click', function() {
        fetch(`/emails/${email_id}`)
        .then(response => response.json())
        .then(email => {
            compose_email();
            original_recipients = email['recipients'];
            document.querySelector('#compose-recipients').value = `${email['sender']}`;
            document.querySelector('#compose-subject').value = `Re: ${email['subject']}`;
            document.querySelector('#compose-body').value = `\n\nOn ${email['timestamp']} ${email['sender']} wrote: \n${email['body']}`;
            });
        });

        //mark as unread button
        document.querySelector('#unreadbtn').addEventListener('click', function() {
            fetch(`/emails/${email_id}`, {
            method: "PUT",
            body: JSON.stringify({
                read: false
            })
            })
            .then(() => {load_mailbox('inbox')})
        })
    });
}