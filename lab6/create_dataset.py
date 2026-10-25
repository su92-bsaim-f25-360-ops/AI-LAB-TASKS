"""Create corpus.json and queries.json (run once).

Each document is expanded to roughly 150-250 words. The evidence sentences from
the starter dataset are kept unchanged; neighbouring distractor sentences were
added around them so that chunking strategies can actually be compared.
"""
import json
from pathlib import Path

rows = [
    ("late",
     "Course work in the department follows a fixed calendar that is published at the start of each term. "
     "Every assignment lists its opening date, its closing date and the marks it carries. Students should read "
     "these details carefully because the same rules are applied to the whole class. Group projects are handed in "
     "once per team, and every member must be named on the cover page. "
     "Late submission is normally penalized. "
     "Illness extensions require medical evidence before the deadline. "
     "Technical problems with the learning portal are handled separately, and a screenshot of the error message "
     "should be kept by the student. The teaching office answers questions about the grading scale on weekdays "
     "between nine and four. Marks are released within two weeks of the closing date, and students may ask for a "
     "second marking of a paper if they believe a mistake has been made. Feedback comments are written by the "
     "instructor and are visible in the portal after the marks are published. Students who miss an examination "
     "should contact their programme coordinator, who keeps a record of all such cases for the board of studies.",
     "Illness extensions require medical evidence before the deadline."),
    ("password",
     "The university network gives every student one account that works for email, the library and the learning "
     "portal. Accounts are created during admission and stay active until a few months after graduation. "
     "Passwords should be at least twelve characters long and should not repeat an older password. "
     "Reset a forgotten password using the recovery link. "
     "Never share recovery codes. "
     "The help desk is located in the main building and is open during working hours, but it cannot read or "
     "change a password for anyone. Students who change their phone number should update it in the profile "
     "page so that verification messages arrive correctly. Shared computers in the laboratories sign users out "
     "after fifteen minutes of inactivity, and files saved on the local disk are removed every night. Wireless "
     "access is available across the campus, and guests can request a temporary visitor account from the "
     "reception desk. Software licences for design tools are provided free of charge to enrolled students "
     "through the campus catalogue.",
     "Reset a forgotten password using the recovery link."),
    ("assignment",
     "Teachers publish coursework through the digital platform of the university, where each course has its own "
     "page with the syllabus, the lecture slides and the lab manuals. Announcements about room changes and quiz "
     "dates also appear on the course page, and students are expected to check it regularly. "
     "Upload assignments through the learning portal. "
     "Submit the final file as a PDF. "
     "File names should contain the roll number and the course code so that the instructor can sort the "
     "submissions easily. Large files such as videos should be shared through a link, and the link must stay "
     "valid until the marks are released. Plagiarism reports are generated automatically for written work, and "
     "a similarity score above the limit set by the instructor leads to a review. Students can open the "
     "assignment page again after submitting to confirm that the file was received. Laboratory reports that "
     "include source code should also list the repository address and the version of the programming language "
     "used during the experiments.",
     "Upload assignments through the learning portal."),
    ("contractor",
     "The human resources handbook explains the working arrangements for everyone who is paid by the company. "
     "Regular employees receive a fixed salary, annual leave and medical cover, and their working hours are set "
     "by the department head. Remote work for employees needs a written approval from the line manager and is "
     "reviewed every six months. "
     "Contractors can work remotely only if the signed contract permits it. "
     "Employee rules do not apply to contractors. "
     "Contractors are paid against invoices, and the payment schedule is written in the agreement. They use "
     "their own equipment unless the agreement says otherwise, and access to internal systems is closed when "
     "the contract ends. Questions about the renewal of an agreement go to the procurement office. Visitors "
     "who are neither staff nor contractors must be registered at the front gate and must wear a badge at all "
     "times. Safety training is mandatory for anyone who enters the production area, whatever their type of "
     "engagement with the company, and the training record is checked at the gate every morning.",
     "Contractors can work remotely only if the signed contract permits it."),
    ("printer",
     "Office printers are shared by each floor and are maintained by the facilities team once a month. "
     "Paper trays should be filled with standard A4 sheets, and special paper such as card or labels must be "
     "loaded in the manual tray at the side. Users can send a document to any printer on the floor, but jobs "
     "that stay in the queue for more than a day are deleted automatically. "
     "For blank printer pages, check ink levels and run the cleaning utility. "
     "Print a test page afterwards. "
     "Paper jams are cleared by opening the rear cover and pulling the sheet gently in the direction of the "
     "paper path. Colour printing is limited to the marketing department to control costs, and double sided "
     "printing is the default setting for all black and white jobs. Replacement cartridges are stored in the "
     "supply cupboard, and the facilities team records every cartridge that is taken. Scanners attached to the "
     "printers send files to the email address of the person who is signed in at the device.",
     "For blank printer pages, check ink levels and run the cleaning utility."),
]

docs = {doc: text for doc, text, evidence in rows}
evidence = {doc: e for doc, text, e in rows}
for doc, text, e in rows:
    assert e in text, doc
    assert 150 <= len(text.split()) <= 250, (doc, len(text.split()))

questions = [
    ("What is required for illness extensions?", "late", "dev"),
    ("How do I reset a forgotten password?", "password", "dev"),
    ("Where do I upload assignments?", "assignment", "dev"),
    ("Can contractors work remotely?", "contractor", "dev"),
    ("What do I do for blank printer pages?", "printer", "test"),
    ("How can I recover my login access?", "password", "test"),
    ("How should I hand in my coursework?", "assignment", "test"),
    ("What proof is needed when I was ill?", "late", "test"),
    ("What are tomorrow's flight prices?", None, "test"),
    ("Who won the football match?", None, "test"),
]
queries = [dict(query=q, doc=doc, evidence=evidence[doc] if doc else None, split=split)
           for q, doc, split in questions]

for name, data in [("corpus.json", docs), ("queries.json", queries)]:
    if Path(name).exists():
        raise FileExistsError("Refusing to overwrite " + name)
    Path(name).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
print("Created corpus.json and queries.json")
for d, t in docs.items():
    print(d, len(t.split()), "words")
