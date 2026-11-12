# Presentation verification, 11 November 2026

- Nine slides fit 1280 x 720 and 1440 x 900 desktop viewports.
- Mobile layout checked at 390 x 844; decorative overflow corrected.
- Next button, keyboard navigation after button focus, overview navigation and notes tested.
- Both WAVs decode and advance; playing one pauses the other; navigating pauses audio; waveform highlighting advances.
- Exact source audio hashes, 30-second durations and local dependencies pass scripts/test_presentation_website.py.
- PDF has nine nonempty pages and correct dataset/training counts; listening page visually inspected.
- Browser console produced no messages during final navigation checks.
- Headless fullscreen did not enter fullscreen; browser F11 is documented as fallback. Classroom projector, speakers and live rehearsal remain unchecked.
