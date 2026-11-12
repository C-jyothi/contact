
const API_URL = (
    import.meta.env.VITE_API_URL || "http://localhost:8000"
).replace(/\/$/, "");


// API 1: Add a contact
export async function addContact(contact) {

    const response = await fetch(`${API_URL}/contacts`, {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(contact)

    });

    if (!response.ok) {
        throw new Error("Unable to add contact");
    }

    return response.json();
}


// API 2: Get all contacts
export async function getContacts() {

    const response = await fetch(`${API_URL}/contacts`);

    if (!response.ok) {
        throw new Error("Unable to load contacts");
    }

    return response.json();
}


// API 3: Delete a contact
export async function deleteContact(id) {

    const response = await fetch(
        `${API_URL}/contacts/${id}`,
        {
            method: "DELETE"
        }
    );

    if (!response.ok) {
        throw new Error("Unable to delete contact");
    }

    return response.json();
}
