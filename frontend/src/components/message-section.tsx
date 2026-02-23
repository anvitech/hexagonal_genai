import { useState } from 'react';

export default function MessageSection({
  conversationId,
  setResponseContent
}: Readonly<{conversationId: string, setResponseContent: (string: string) => void}>) {
  const [message, setMessage] = useState('');

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => setMessage(e.target.value);

  const sendMessageHandler = (e: React.FormEvent) => {
    e.preventDefault();

    // Send the message
    const url = import.meta.env.VITE_API_BASE_URL;
    fetch(`${url}/conversations/${conversationId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message }),
    })
    .then((response) => response.json())
    .then((data) => setResponseContent(data.response))
    .catch((error) => console.error(error));

    // Reset the form
    setMessage('');
  };

  return (
    <form className="message-section">
      <textarea
        placeholder="Tapez votre message ici..."
        name="message-content"
        aria-label="Message"
        value={message}
        onChange={handleChange}
      >
      </textarea>
      <button type="submit" onClick={sendMessageHandler}>Envoyer</button>
    </form>
  );
}