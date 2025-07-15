import { useState } from 'react';
import './App.css';
import "@chatscope/chat-ui-kit-styles/dist/default/styles.min.css";
import {
  MainContainer,
  ChatContainer,
  MessageList,
  Message,
  MessageInput,
  TypingIndicator
} from "@chatscope/chat-ui-kit-react";

const API_URL = "http://localhost:8000/chat";

function App() {
  const [typing, setTyping] = useState(false);
  const [messages, setMessages] = useState([
    {
      message: "Hello, ask me anything, I am here to help!",
      sender: "Your AI Bot"
    }
  ]);

  const handleSend = async (message) => {
    const newMessage = {
      message: message,
      sender: "user",
      direction: "outgoing"
    }
    const newMessages = [...messages, newMessage];

    setMessages(newMessages);

    setTyping(true);

    await processMessageToBackend(message, newMessages); 
  }

  async function processMessageToBackend(userMessage, chatHistory){
    try{
        const response = await fetch (API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({message: userMessage})
      });

      const data = await response.json();

      
      setMessages([
        ...chatHistory, 
        {
          message: data.response,
          sender: 'Your AI Bot',
          direction: 'ingoing'
        }
      ]);

    } catch(error) {
      setMessages([
        ...chatHistory,
        {
          message: "❌ Error contacting backend.",
          sender: "Your AI Bot"
        }
      ]);
    } finally {
      setTyping(false);
    }
  }

  return (
      <div>
        <div style={{position: "relative", height: "800px", width:"700px"}}>
          <MainContainer>
            <ChatContainer>
              <MessageList
              scrollBehavior='smooth'
              typingIndicator={typing ? <TypingIndicator content = "Bot is typing..."/> : null}>
                {messages.map((message, i) => {
                  return <Message key={i} model={message}/>
                })}
              </MessageList>
              <MessageInput placeholder = 'Type message here' onSend={handleSend}/>
            </ChatContainer>
          </MainContainer>
        </div>
      </div>
  )
}

export default App