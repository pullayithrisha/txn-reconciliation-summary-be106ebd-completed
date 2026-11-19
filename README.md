## Task Overview

A fintech payments team runs a nightly job that turns a raw export of card transactions into a clean daily summary for each account. The raw file is a little messy: money amounts arrive as text, dates arrive as plain strings, and the transaction status has mixed capitalization and stray spaces, so the same outcome can look like ' Settled ', 'SETTLED', or 'settled'. A few rows are also missing an amount.

Right now the reconciliation code loads the file but leaves these columns as raw text, so the totals are wrong, successful transactions are not identified consistently, and the per-day, per-account summary does not add up. Your job is to clean and shape the data so the summary correctly counts and totals only the settled transactions, and to finish a small vectorized flag that marks whether each transaction settled.

## Objectives

- Load the shipped CSV so that money amounts become numeric and dates become real datetime values instead of plain text, because text columns make totals and date grouping impossible.
- Normalize the status text so that mixed casing and extra spaces (like ' Settled ' and 'SETTLED') all count as the same outcome when deciding which transactions settled.
- Build a vectorized flag that marks each transaction as settled or not without looping over rows, so downstream filtering and counting stay fast and simple.
- Filter the data with a boolean mask so only settled transactions flow into the summary, and make sure rows with a missing amount do not corrupt the totals.
- Produce a grouped summary by date and account that reports the correct total settled amount and the correct count of settled transactions for each group.

## Helpful Tips

- Review the loaded dtypes right after reading the file; if amounts or dates are still text, the later math and grouping will quietly produce wrong answers.
- Consider how whitespace and capitalization in the status column can make equal values look unequal, and clean the text before comparing.
- Explore how a boolean condition over an entire column can create a settled flag in one step instead of checking rows one at a time.
- Think about what should happen to a transaction with a missing amount when you sum totals, and handle it so it does not turn a valid total into a missing value.
- Analyze the grouping keys carefully so each account's daily total and count reflect only the settled transactions for that exact day.

## How to Verify

- Confirm that after loading, the amount column is numeric and the date column is a datetime type rather than plain text.
- Check that the settled flag marks only genuinely settled transactions, regardless of casing or surrounding spaces.
- Verify that the summary totals match the expected settled amounts per account per day and that counts reflect only settled transactions.
- Ensure rows with a missing amount do not break the totals and that the full pytest suite passes after your fixes.
