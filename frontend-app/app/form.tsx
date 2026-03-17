"use client";
import { useState } from "react";

export default function Form() {
  const [form, setForm] = useState({
    name: "",
    email: "",
    dob: "",
    birth_time: "",
    birth_location: "",
    experience_date: "",
    experience_time: "",
    experience_location: "",
    substance: "",
    intention: "",
  });
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResponse(null);

    // Build the payload, converting empty optional strings to null
    const payload = {
      ...form,
      name: form.name || null,
      email: form.email || null,
      substance: form.substance || null,
      intention: form.intention || null,
    };

    try {
      const res = await fetch("/api/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Something went wrong");
      }

      const data = await res.json();
      setResponse(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <form onSubmit={handleSubmit}>

        {/* Optional contact info */}
        <fieldset>
          <legend>Contact Info (optional)</legend>

          <div>
            <label htmlFor="name">Name</label>
            <input
              id="name"
              name="name"
              value={form.name}
              onChange={handleChange}
            />
          </div>

          <div>
            <label htmlFor="email">Email</label>
            <input
              id="email"
              name="email"
              type="email"
              value={form.email}
              onChange={handleChange}
            />
          </div>
        </fieldset>

        {/* Birth information */}
        <fieldset>
          <legend>Birth Information</legend>

          <div>
            <label htmlFor="dob">Date of Birth</label>
            <input
              id="dob"
              name="dob"
              type="date"
              value={form.dob}
              onChange={handleChange}
              required
            />
          </div>

          <div>
            <label htmlFor="birth_time">Birth Time</label>
            <input
              id="birth_time"
              name="birth_time"
              type="time"
              value={form.birth_time}
              onChange={handleChange}
              required
            />
          </div>

          <div>
            <label htmlFor="birth_location">Birth Location</label>
            <input
              id="birth_location"
              name="birth_location"
              value={form.birth_location}
              onChange={handleChange}
              placeholder="City, State/Country"
              required
            />
          </div>
        </fieldset>

        {/* Experience information */}
        <fieldset>
          <legend>Experience Information</legend>

          <div>
            <label htmlFor="experience_date">Experience Date</label>
            <input
              id="experience_date"
              name="experience_date"
              type="date"
              value={form.experience_date}
              onChange={handleChange}
              required
            />
          </div>

          <div>
            <label htmlFor="experience_time">Experience Time</label>
            <input
              id="experience_time"
              name="experience_time"
              type="time"
              value={form.experience_time}
              onChange={handleChange}
              required
            />
          </div>

          <div>
            <label htmlFor="experience_location">Experience Location</label>
            <input
              id="experience_location"
              name="experience_location"
              value={form.experience_location}
              onChange={handleChange}
              placeholder="City, State/Country"
              required
            />
          </div>

          <div>
            <label htmlFor="substance">Substance (optional)</label>
            <input
              id="substance"
              name="substance"
              value={form.substance}
              onChange={handleChange}
            />
          </div>

          <div>
            <label htmlFor="intention">Intention (optional)</label>
            <textarea
              id="intention"
              name="intention"
              value={form.intention}
              onChange={handleChange}
            />
          </div>
        </fieldset>

        <button type="submit" disabled={loading}>
          {loading ? "Submitting..." : "Submit"}
        </button>
      </form>

      {response && <p>{response.detail}</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}
    </>
  );
}
