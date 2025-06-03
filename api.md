# API Documentation: SRS Assistant Endpoints

This API provides endpoints for managing Software Requirements Specification (SRS) sessions and generating SRS documents using AI.

---

## 1. Start SRS Session

**POST** `/start_srs_session`

Start a new SRS Q&A session. Returns a session ID and the first AI-generated question.

### Request

- No body required.

### Response

```json
{
  "session_id": "string",
  "question": "string",
  "reason": "string"
}
```

### Example (cURL)

```bash
curl -X POST http://localhost:8000/start_srs_session
```

---

## 2. Continue SRS Q&A

**POST** `/continue_srs/{session_id}`

Continue the SRS Q&A by sending a user response. Returns a streamed AI response (reasoning and next question).

### Path Parameters

- `session_id`: The session ID from `/start_srs_session`.

### Request Body

```json
{
  "response": "string"
}
```

### Response

- **Streaming text/plain**: AI reasoning and next question, streamed character by character.

### Example (cURL)

```bash
curl -X POST http://localhost:8000/continue_srs/{session_id} \
  -H "Content-Type: application/json" \
  -d '{"response": "<your answer>"}'
```

---

## 3. Get SRS Session Data

**GET** `/srs_session/{session_id}`

Retrieve the current state of an SRS session.

### Path Parameters

- `session_id`: The session ID.

### Response

- Returns the full session object (see your models for details).

### Example (cURL)

```bash
curl -X GET http://localhost:8000/srs_session/{session_id}
```

---

## 4. Regenerate Full SRS (with Style/Tone)

**POST** `/srs/{session_id}/generate`

Regenerate the full SRS document for a session, optionally specifying style and tone.

### Path Parameters

- `session_id`: The session ID.

### Request Body (optional)

```json
{
  "style": "string (optional)",
  "tone": "string (optional)"
}
```

### Response

```json
{
  "srs": "string"
}
```

### Example (cURL)

```bash
curl -X POST http://localhost:8000/srs/{session_id}/generate \
  -H "Content-Type: application/json" \
  -d '{"style": "formal", "tone": "professional"}'
```

---

## 5. Get Latest Generated SRS

**GET** `/srs/{session_id}/latest`

Retrieve the most recently generated SRS document for a session.

### Path Parameters

- `session_id`: The session ID.

### Response

```json
{
  "srs": "string"
}
```

### Example (cURL)

```bash
curl -X GET http://localhost:8000/srs/{session_id}/latest
```

---

## 6. Regenerate SRS with Custom Prompt

**POST** `/srs/{session_id}/custom_prompt`

Regenerate the SRS using a custom freeform prompt.

### Path Parameters

- `session_id`: The session ID.

### Request Body

```json
{
  "prompt": "string"
}
```

### Response

```json
{
  "srs": "string"
}
```

### Example (cURL)

```bash
curl -X POST http://localhost:8000/srs/{session_id}/custom_prompt \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Make it concise and bullet-pointed."}'
```

---

## Error Responses

- All endpoints may return errors in the following format:

```json
{
  "detail": "Error message here."
}
```

---

## Notes

- Replace `localhost:8000` with your actual host/port if different.
- All endpoints assume the FastAPI app is running and accessible.
- For streaming endpoints, you may need a client that supports streamed responses.
