
import { useState, useEffect } from "react";

import {
    addContact,
    getContacts,
    deleteContact
} from "./api";


function App() {

    // Store contact form information.
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [phone, setPhone] = useState("");

    // Store all contacts.
    const [contacts, setContacts] = useState([]);

    // Store messages.
    const [message, setMessage] = useState("");

    // Load contacts when the page opens.
    useEffect(() => {

        loadContacts();

    }, []);


    // Get all contacts from backend.
    async function loadContacts() {

        try {

            const data = await getContacts();

            setContacts(data);

        } catch (error) {

            setMessage(error.message);

        }
    }


    // Add a new contact.
    async function handleSubmit(event) {

        event.preventDefault();

        try {

            const contact = {
                name: name,
                email: email,
                phone: phone
            };

            await addContact(contact);

            setMessage("Contact added successfully!");

            // Clear the form.
            setName("");
            setEmail("");
            setPhone("");

            // Refresh contact list.
            await loadContacts();

        } catch (error) {

            setMessage(error.message);

        }
    }


    // Delete a contact.
    async function handleDelete(id) {

        try {

            await deleteContact(id);

            setMessage("Contact deleted successfully!");

            await loadContacts();

        } catch (error) {

            setMessage(error.message);

        }
    }


    return (

        <div className="container">

            <h1>My Contact Book</h1>

            <p>Save and manage your contacts easily.</p>


            {/* Contact form */}

            <div className="form-box">

                <h2>Add New Contact</h2>

                <form onSubmit={handleSubmit}>

                    <input
                        type="text"
                        placeholder="Enter name"
                        value={name}
                        onChange={(event) =>
                            setName(event.target.value)
                        }
                        required
                    />

                    <input
                        type="email"
                        placeholder="Enter email"
                        value={email}
                        onChange={(event) =>
                            setEmail(event.target.value)
                        }
                        required
                    />

                    <input
                        type="tel"
                        placeholder="Enter phone"
                        value={phone}
                        onChange={(event) =>
                            setPhone(event.target.value)
                        }
                        required
                    />

                    <button type="submit">
                        Add Contact
                    </button>

                </form>

            </div>


            {/* Success or error message */}

            {message && <p role="status">{message}</p>}


            {/* Display contacts */}

            <div className="contact-list">

                <h2>My Contacts</h2>

                {contacts.length === 0 ? (

                    <p>No contacts available.</p>

                ) : (

                    contacts.map((contact) => (

                        <div
                            className="contact-card"
                            key={contact.id}
                        >

                            <h3>{contact.name}</h3>

                            <p>Email: {contact.email}</p>

                            <p>Phone: {contact.phone}</p>

                            <button
                                className="delete-button"
                                onClick={() =>
                                    handleDelete(contact.id)
                                }
                            >
                                Delete
                            </button>

                        </div>

                    ))

                )}

            </div>

        </div>

    );

}


export default App;
