# CLAUDE.md — alpha-site

> נוצר על ידי הסקיל `repo-bootstrap` v1.1.0 בתאריך 15/11/2026.
> **הקובץ הזה הוא ההגנה האמיתית של הריפו.** אין הגנת שרת על `main` (GitHub Free + ריפו פרטי),
> ולכן הכללים כאן הם מה שמונע בלגן. עדכן אותו כשהפרויקט משתנה.

## מה זה

Public bilingual site explaining the personalised neoantigen vaccine project for Alpha

## Stack

`static-vite`

## פקודות

<!-- מולא אוטומטית לפי ה-stack; עדכן כשמשתנה -->

| מטרה | פקודה |
|---|---|
| הרצה מקומית | `npm run dev` |
| build | `npm run build` |
| תצוגה מקדימה של build | `npm run preview` |

## כללי עבודה — מחייבים

1. **אסור push ישיר ל-`main`.** תמיד `feature/<name>` ואז PR. יש `pre-push` hook מקומי
   שחוסם, אבל הוא חל רק על clone שהוגדר בו `core.hooksPath` — הכלל הזה גובר עליו תמיד.
2. **Conventional Commits בלבד:** `<type>(<scope>): <subject>` —
   `feat` `fix` `docs` `style` `refactor` `perf` `test` `build` `ci` `chore` `revert`.
   subject בציווי, עד ~72 תווים.
3. **אפס סודות ואפס פרטי תשתית ב-git.** סודות = טוקנים, סיסמאות, מפתחות.
   פרטי תשתית = כתובות IP פנימיות, פורט SSH, נתיבי בית עם שם משתמש (`/home/<user>`),
   hostnames פנימיים (`.local`, `.lan`, `.ts.net`), שמות משתמש ופרטי קשר אישיים.
   חל גם על הודעות commit, תיאורי PR ו-issues.
   - שמות משתנים ב-`.env.example`; ערכים ב-`.env` המקומי (לא נכנס ל-git). המקור: סקיל `credentials-vault`.
   - בתיעוד ובדוגמאות: `192.0.2.10`, `example.com`, `$HOME/...`, `<user>`.
   - חריגה מכוונת ומאושרת: הערה `gitleaks:allow` בסוף השורה, עם נימוק ב-PR.
   - `pre-commit` hook חוסם סודות מקומית; הבדיקה `secret-scan` ב-CI תופסת גם פרטי תשתית.
     פירוט: `coding-conventions` §5.
4. **קרא לפני שאתה כותב.** לפני שינוי בקובץ קיים — קרא אותו והתאם לסגנון הקיים.
5. **אמת לפני שאתה מדווח.** אחרי שינוי: build / lint / הרצה. אל תכתוב "בוצע" בלי אימות.
6. **אל תמציא.** חסר נתון (endpoint, פורט, מבנה טבלה)? בדוק בקוד, בסקיל, או שאל את עידן.
7. **אסור למזג PR כשהבדיקה `secret-scan` אדומה.** בריפו פרטי גיטהאב לא חוסם את המיזוג — הכלל הזה כן.
   ממצא ב-commit קודם של הענף: לשכתב את הענף (amend / rebase + force-push באישור עידן),
   לא להוסיף commit תיקון — ה-commit הישן נשאר גלוי ב-PR.

## אחרי clone חדש

```bash
git config core.hooksPath .githooks
```
בלי זה ה-hooks לא פעילים ב-clone הזה. בסשן ענן זה השלב הראשון.

## סקילים רלוונטיים

| נושא | סקיל |
|---|---|
| מוסכמות קוד (מקור אמת) | `coding-conventions` |
| branch / commit / PR / merge | `git-workflow` |
| סקירת קוד, tags, releases | `code-review` |
| סודות והרשאות | `credentials-vault` |

## משתני סביבה

ראה `.env.example` — שמות בלבד. ערכים לעולם לא נכנסים לריפו.

## Deploy

<!-- TODO: איך מדפלים, לאן, ומה בדיקת העשן שמאשרת הצלחה -->

## אסור לגעת

<!-- TODO: נתיבים או קבצים שדורשים אישור מפורש מעידן לפני שינוי -->
