# AI Customer Support Agent - Solution Design Document

## 1. Role Chosen: Customer Support Agent AI

**Reason:**
Customer support is repetitive but crucial. Automating first-line customer conversations saves human effort, improves speed, and creates better user experiences.
AI can handle the majority of simple queries, escalate edge cases, and stay online 24/7.

## 2. Core Responsibilities

- **Respond to User Queries:** Answer customer questions promptly and accurately.

- **Follow-up with Users:** Ask for clarifications or further information if needed.

- **Maintain Short-Term Memory:**  Store and reference the last 10 messages per user (Will handle better in the future).

- **Simulate Multi-User Conversations:**   Randomly assign a simulated user ID to each session (Will handle better in the future for authenticated users).

- **Handle Session State:**    Maintain user context between follow-up interactions (Simulating memory).

## 3. High-Level Architecture

```bash
User
   ⇅ 
FastAPI App
   ⇅ 
Gemini AI Model API
   ⇅ 
In-memory User Context (in-memory yet.)

```

## 4. Third-Party APIs & Integrations

- **Google Cloud Gemini API-** | Power the AI conversation and generate responses.

## 5. Agent Actions & Automations

- **Respond to user questions**   Use Gemini API to generate responses based on user prompts.
- **Ask for clarification automatically** Analyze Gemini responses to determine when to follow-up.
- **Remember previous messages**  Store the last 10 interactions in memory, per simulated user.
- **Simulate multiple users** Randomly assign from a pool of 2-3 fake User IDs per session.
- **Reset memory when needed**    Keep only 10 messages, and discard older ones automatically.

## 6. Future feature improvemnts

- **Security:** For now we mocked users but in real production, user IDs should not be passed through plain API requests. Session tokens, cookies, or OAuth should be used.

- **Scalability:** For now, we used in-memory storage for MVPs But in the future we'll implement Database (PostgreSQL), Redis or a managed cache.
