import os

RAW_DIR = "socials_data/personalities/plato/raw"

def clean_republic():
    filepath = os.path.join(RAW_DIR, "the_republic.txt")
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    # The marker I tried before failed likely due to exact whitespace issues.
    # I'll just look for the second occurrence of "PERSONS OF THE DIALOGUE" which is the real start.

    marker = "PERSONS OF THE DIALOGUE."
    first_idx = text.find(marker)
    if first_idx != -1:
        # Look for the second one
        second_idx = text.find(marker, first_idx + 1)
        if second_idx != -1:
            # Backtrack to "THE REPUBLIC" just before it?
            # Or just start there.
            # Let's find "THE REPUBLIC." just before it.
            start_marker = "THE REPUBLIC."
            real_start = text.rfind(start_marker, 0, second_idx)

            if real_start != -1:
                content = text[real_start:]
                # We already stripped the footer in the previous pass, so no need to strip again unless we want to be safe.
                # But wait, the previous pass FAILED to find the start marker, so it fell back to removing the PG header only.
                # So the PG footer is already gone?
                # "Cleaned the_republic.txt" was printed, so it did something.
                # It fell back to PG start marker.

                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                print("Refined cleaning for the_republic.txt")
                return

    print("Could not refine cleaning for the_republic.txt")

if __name__ == "__main__":
    clean_republic()
