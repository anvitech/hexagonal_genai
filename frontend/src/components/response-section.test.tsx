import { render, screen } from '@testing-library/react';
import ResponseSection from './response-section';


describe('ResponseSection', () => {
  const conversationId = 'conversation-id';
  const responseContent = {
    history: [
      { id: '1', role: 'user', content: 'Hello' },
      { id: '2', role: 'assistant', content: 'World' },
    ],
  };

  test('renders the conversation ID', () => {
    render(<ResponseSection conversationId={conversationId} responseContent={responseContent} />);
    expect(
      screen.getByRole(
        'heading', { name: 'Conversation: ' + conversationId }
      )
    ).toHaveTextContent('Conversation: ' + (conversationId));
  });

  test('renders the response content', () => {
    render(<ResponseSection conversationId={conversationId} responseContent={responseContent} />);
    const responseContentElement = screen.getByText('user: Hello');
    expect(responseContentElement).toBeInTheDocument();
    expect(responseContentElement.nextSibling?.textContent).toBe('assistant: World');
  });

  test('renders the response content as a string when it is not an object', () => {
    const responseContentString = 'This is a string response';
    render(<ResponseSection conversationId={conversationId} responseContent={responseContentString} />);
    expect(screen.getByText(responseContentString)).toBeInTheDocument();
    expect(screen.queryByText('user: Hello')).not.toBeInTheDocument();
  });
});