import userEvent from '@testing-library/user-event';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';

import MessageSection from './message-section';


describe('MessageSection', () => {
  test('should render with all props provided', () => {
    const setResponseContent = vi.fn();
    render(
      <MessageSection
        conversationId="conversation-id"
        setResponseContent={setResponseContent}
      />
    );

    // Assert that the component renders without errors
    expect(screen.getByPlaceholderText('Tapez votre message ici...')).toBeInTheDocument();
  });

  test('updates state correctly when textarea value changes', () => {
    const setResponseContent = vi.fn();
    render(
      <MessageSection
        conversationId="conversation-id"
        setResponseContent={setResponseContent}
      />
    );

    const testMessage = 'Hello, world!';

    // Get the textarea
    const textarea = screen.getByRole('textbox', { name: /message/i });

    // Assert the initial state (optional, but good practice)
    expect(textarea).toHaveValue('');

    // Triggers the onChange handler and updates the component's internal state.
    fireEvent.change(textarea, {
      target: {
        value: testMessage // Simulate the new value the event carries
      }
    });

    // Check if the element's value property reflects the state update.
    expect(textarea).toHaveValue(testMessage);
  });

  test('sends a POST request with the message content and updates the response content state', async () => {
    // Setup user event instance
    const user = userEvent.setup();

    // Create a mock implementation that returns a Promise resolved with a mock Response object
    const mockResponseData = { response: 'Response content' };
    const fetchSpy = vi.spyOn(globalThis, 'fetch').mockResolvedValue({
        ok: true,
        json: async () => mockResponseData,
    } as Response);

    // Render the component
    const setResponseContent = vi.fn();
    render(
      <MessageSection
        conversationId="conversation-id"
        setResponseContent={setResponseContent}
      />
    );

    // Simulate user interaction
    const textarea = screen.getByRole('textbox', { name: /message/i });
    const button = screen.getByRole('button', { name: /envoyer/i });

    fireEvent.change(textarea, { target: { value: 'Hello' } });
    await user.click(button);

    // --- Assertions ---

    // Wait for the asynchronous fetch call to complete before asserting the call details
    await waitFor(() => {
      expect(fetchSpy).toHaveBeenCalledWith(
        `${import.meta.env.VITE_API_BASE_URL}/conversations/conversation-id`, // Corrected URL structure
        expect.objectContaining({
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          // Ensure the body is correctly serialized JSON
          body: JSON.stringify({ message: 'Hello' }), // Assuming conversationId is also sent
        })
      );
    });

    // Use waitFor to ensure the promise chain from fetch -> .json() -> setResponseContent has completed
    await waitFor(() => {
      // Assert that the response content state was updated correctly
      expect(setResponseContent).toHaveBeenCalledWith('Response content');
    });

    // Clean up the mock
    fetchSpy.mockRestore();
  });
});