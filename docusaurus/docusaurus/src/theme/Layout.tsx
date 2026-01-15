import React from 'react';
import Layout from '@theme-original/Layout';
import ChatBotLayout from '../components/ChatBotLayout';

export default function LayoutWrapper(props) {
  return (
    <Layout {...props}>
      <ChatBotLayout>
        {props.children}
      </ChatBotLayout>
    </Layout>
  );
}