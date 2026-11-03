# Chase dossier: fact-check log

*Nov 2026. This file records how `profile.md` and `system-prompt.md` were checked and what changed as a result. The check was adversarial: the draft was treated as if it contained errors, and sources were fetched again rather than taken on trust from the research notes.*

## Method

| Layer | What was re-checked | How |
|---|---|---|
| 1. Diary of a CEO quotes | Every line attributed to [S31] (Dec 2024) and [S37] (Mar 2026) | Downloaded both full YouTube-caption transcripts from GitHub. Extracted **every quoted string** in both files and matched each against the raw text with [`tools/quotecheck.py`](../../tools/quotecheck.py), ignoring case and punctuation. |
| 2. Behavioral Table of Elements | Scoring scale, threshold, layout, modifiers | Downloaded Hughes's own 2022 BTE PDF (© 2018–2022) and read the key directly. |
| 3. Biography, books, courses, podcast table (§1–2) | Names, dates, titles, critics' claims | An independent agent re-searched each claim from scratch. |
| 4. Frameworks, playbook and science claims (§3, §4, §6, §10) | Non-DOAC quotes, model details, research citations | A second independent agent re-searched each claim. The research citations were then checked again by direct search. |

**Limits.** The environment blocked full-page fetches of shortform.com, goodreads.com, amazon.com, chasehughes.com, nci.university, jordanharbinger.com, theartofcharm.com, youtube.com and reddit.com. Claims from those sites rest on search-result excerpts and stay marked ◐.

## Results

### Layer 1: transcript quotes
- **About 250 quoted fragments matched the transcripts.** The misses that remain are labels, example scripts, or quotes correctly attributed to other sources.
- **Removed: two lines the research notes had attributed to Diary of a CEO but which aren't in either transcript:**
  - "I'm gonna be the most comfortable person in this environment…"
  - "…And I'm gonna move slower"

  They were replaced with the verified "can you move slower than the other people in the room… adjusting the speed limit on your body."
- **Corrected toward verbatim wording (about 20 lines).** The draft had tidied his phrasing. Examples:
  - "fewer questions you should ask" → "the less questions you need to be asking"
  - "We deal in likelihood" → "If you're in body language, you deal in likelihood. That's all we deal in."
  - "contracts written in a child's voice" → "contracts that were written in a child's voice"
  - The frame-setting scripts, the product test, the wife/business-trip example and others.
- **Fixed episode attribution.** Several FATE, novelty and script lines belong to episode 2 (Mar 2026), not episode 1.
- **Confirmed one anecdote is staged.** The "dog knocked the coffee over" sales opener is faked on purpose: "they pretend like their dog just knocked a drink over."
- **Corrected one meaning.** "Slowest moving person in the room" refers to the most *confident* person, not "who holds authority."

### Layer 2: BTE
- **Confirmed verbatim:**
  - the 1–4 Deception Rating Scale;
  - "rated per question and answer scenario";
  - deception is "highly likely" at "more than 11 points" (the side key says "11 or more… per cluster");
  - behaviors run left to right from least to most stressful/deceptive.
- **Added:** the red-letter and blue-letter modifiers, the gesture types and the deception timeframe.
- **Downgraded ✅ → ◐:** the lip-compression quote. Its source PDF now returns Access Denied.

### Layer 3: biography, books, podcasts
- **Removed:**
  - The foreword and co-author credits for *Excellence in NLP and Life Coaching* (a Richard Nongard book) and *Civilian Mission*. There is no evidence for either.
  - A "recycled, but enhanced" review quote that couldn't be found.
- **Corrected:**
  - The "no more than any other jail guard" quote isn't in any source. It was rewritten as Clizbe's actual claim (about 3.5 years as a jail guard, then quartermaster). Antonova's separate points were attributed to her.
  - Target Intelligence ch. 10 has its own title, which is now used.
  - Avery program: "up to $50,000" → one client says she paid $50,000.
  - The free authority tool is the "Hughes Authority Self-Assessment Matrix." It is also the "Authority inventory" he mentions on Diary of a CEO.
  - Art of Manliness #875 is dated 27 Feb 2023, and its URL was fixed.
- **Downgraded ✅ → ◐:**
  - retirement year 2019;
  - Behavior Panel start date;
  - NCI tier names;
  - Black Course segments;
  - the Hughes Protocol course;
  - the *Six-Minute X-Ray* resource-sheet names;
  - the NCI education wording;
  - the Training Planner "not an academic work" line, whose referent is also unclear.

### Layer 4: frameworks and science
- **Wrong, now fixed:**
  - **Needs Map fears** (per the Shortform summary):
    - significance → being dismissed or mocked;
    - intelligence → being seen as dumb;
    - pity → being ignored or disbelieved;
    - strength → being disrespected or challenged.
  - **"Authority killers."** Movement and appearance are the first authority *triggers*, the cues that make people read you as an authority. The killers are rapid movement, rapid speech and constant adjusting.
  - **§6.4 contradicted his own quote.** It is *authority* that creates *acceptance*-seeking people, not insecurity creating approval-seekers.
  - **Blink-rate science.** The papers first cited don't say blinking drops during lies. The claim is now cited to Leal & Vrij (2008): fewer blinks *during* the lie, more *after*.
  - **Lie-detection accuracy** is now cited to Bond & DePaulo (2006): about 54%, and experts are no better. Burgoon (2019) is now described accurately: she argues combined cues can help.
  - **The Brennen & Magnussen (2020) article** is an opinion piece ("a blind alley"), not a review. It is now described that way.
- **Misattributed, now fixed:** "if I can just use one word, it's comfort," the composure definition, and the daily journal drill come from Art of Manliness #875 [S30], not Jordan Harbinger #102. The "dominance… fun" list comes from the 2017 interview replayed as JH #768.
- **Removed or paraphrased, because they couldn't be found:**
  - "lowest guy on the totem pole"
  - "we've replaced control with confidence"
  - "the biggest mistake"
  - "each of these pillars bleed into…"
  - "speak their decision language… Don't push novelty…"
  - "does not illustrate all human needs"
  - the London Real "no body language for deception" / "little pile" lines
  - the Medium bait-question wording, replaced with the verified JPost / Women of Impact wording
  - the "change detector" quote, now paraphrased and anchored to his verified "first C is change"
  - the Hanns Scharff "derivative" quote
- **Rewritten from the Shortform definitions:** the Decision Map style descriptions. The pitch lines are now tagged 🧩.
- **Tags lowered to 🧩:** "five seconds after a number" and the blink/lip/hygiene "cluster" trio.
- **Added context:** the five-second window and cluster method mirror *Spy the Lie* (Houston et al.).
- **Ellipsis Progression phase list, "wakeproofing" and "alter personalities":** couldn't be re-confirmed. They are now marked ⚠ and kept only as recognition material.

## Still unverified (do not upgrade without a source)
- The four trust factors after "confidence" (Modern Wisdom).
- The full table of contents of *The Behavior Ops Manual* and *The Ellipsis Manual*.
- Hughes's education claims. Credentials are disputed (§1.2).
- Origin-story details (Pearl Harbor, the car dealership, "failed out of high school"). These conflict with the MMA record.
- The exact wording of anything from Joe Rogan, Shawn Ryan, Danny Jones, PBD and London Real. Only search excerpts were available.
