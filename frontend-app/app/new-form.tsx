"use client";
import { useState, useEffect, useRef } from "react";
import styles from "./form.module.css";

function StarField() {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    for (let i = 0; i < 80; i++) {
      const star = document.createElement("div");
      star.className = styles.star;
      const size = Math.random() * 2 + 0.5;
      star.style.width = `${size}px`;
      star.style.height = `${size}px`;
      star.style.left = `${Math.random() * 100}%`;
      star.style.top = `${Math.random() * 100}%`;
      star.style.opacity = `${Math.random() * 0.5 + 0.1}`;
      star.style.animation = `twinkle ${Math.random() * 4 + 3}s ease-in-out infinite`;
      star.style.animationDelay = `${Math.random() * 5}s`;
      container.appendChild(star);
    }

    return () => {
      container.innerHTML = "";
    };
  }, []);

  return <div ref={containerRef} className={styles.stars} />;
}

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
  const [response, setResponse] = useState<{ detail?: string } | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  function handleChange(
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResponse(null);

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
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Something went wrong");
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className={styles.page}>
      <StarField />

      <div className={styles.container}>
        <h1 className={styles.title}>Cosmic Explorer</h1>
        <p className={styles.subtitle}>Discover the archetypal themes that may shape your upcoming psychedelic journey"</p>
        <div className={styles.divider} />

        <form onSubmit={handleSubmit}>
          {/* Contact (optional) */}
          <fieldset className={styles.fieldset}>
            <legend className={styles.legend}>
              Contact <span className={styles.optionalTag}>optional</span>
            </legend>
            <div className={styles.row}>
              <div className={styles.field}>
                <label htmlFor="name" className={styles.label}>
                  Name
                </label>
                <input
                  id="name"
                  name="name"
                  className={styles.input}
                  value={form.name}
                  onChange={handleChange}
                  placeholder="Your name"
                />
              </div>
              <div className={styles.field}>
                <label htmlFor="email" className={styles.label}>
                  Email
                </label>
                <input
                  id="email"
                  name="email"
                  type="email"
                  className={styles.input}
                  value={form.email}
                  onChange={handleChange}
                  placeholder="you@example.com"
                />
              </div>
            </div>
          </fieldset>

          {/* Birth information */}
          <fieldset className={styles.fieldset}>
            <legend className={styles.legend}>Birth information</legend>
            <div className={styles.field}>
              <label htmlFor="dob" className={styles.label}>
                Date of birth
              </label>
              <input
                id="dob"
                name="dob"
                type="date"
                className={styles.input}
                value={form.dob}
                onChange={handleChange}
                required
              />
            </div>
            <div className={styles.row}>
              <div className={styles.field}>
                <label htmlFor="birth_time" className={styles.label}>
                  Birth time
                </label>
                <input
                  id="birth_time"
                  name="birth_time"
                  type="time"
                  className={styles.input}
                  value={form.birth_time}
                  onChange={handleChange}
                  required
                />
              </div>
              <div className={styles.field}>
                <label htmlFor="birth_location" className={styles.label}>
                  Birth location
                </label>
                <input
                  id="birth_location"
                  name="birth_location"
                  className={styles.input}
                  value={form.birth_location}
                  onChange={handleChange}
                  placeholder="City, Country"
                  required
                />
              </div>
            </div>
          </fieldset>

          {/* Experience information */}
          <fieldset className={styles.fieldset}>
            <legend className={styles.legend}>Experience information</legend>
            <div className={styles.field}>
              <label htmlFor="experience_date" className={styles.label}>
                Experience date
              </label>
              <input
                id="experience_date"
                name="experience_date"
                type="date"
                className={styles.input}
                value={form.experience_date}
                onChange={handleChange}
                required
              />
            </div>
            <div className={styles.row}>
              <div className={styles.field}>
                <label htmlFor="experience_time" className={styles.label}>
                  Experience time
                </label>
                <input
                  id="experience_time"
                  name="experience_time"
                  type="time"
                  className={styles.input}
                  value={form.experience_time}
                  onChange={handleChange}
                  required
                />
              </div>
              <div className={styles.field}>
                <label htmlFor="experience_location" className={styles.label}>
                  Experience location
                </label>
                <input
                  id="experience_location"
                  name="experience_location"
                  className={styles.input}
                  value={form.experience_location}
                  onChange={handleChange}
                  placeholder="City, Country"
                  required
                />
              </div>
            </div>
            <div className={styles.field}>
              <label htmlFor="substance" className={styles.label}>
                Substance <span className={styles.optionalTag}>optional</span>
              </label>
              <input
                id="substance"
                name="substance"
                className={styles.input}
                value={form.substance}
                onChange={handleChange}
                placeholder=""
              />
            </div>
            <div className={styles.field}>
              <label htmlFor="intention" className={styles.label}>
                Intention <span className={styles.optionalTag}>optional</span>
              </label>
              <textarea
                id="intention"
                name="intention"
                className={styles.textarea}
                value={form.intention}
                onChange={handleChange}
                placeholder="What did you hope to explore?"
              />
            </div>
          </fieldset>

          <button
            type="submit"
            className={styles.submitButton}
            disabled={loading}
          >
            {loading ? "Submitting..." : "Begin exploration"}
          </button>
        </form>

        {response && <p className={styles.success}>{response.detail}</p>}
        {error && <p className={styles.error}>{error}</p>}
      </div>
    </div>
  );
}
