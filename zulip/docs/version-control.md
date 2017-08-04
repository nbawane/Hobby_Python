# Version control

## Commit Discipline

We follow the Git project's own commit discipline practice of "Each
commit is a minimal coherent idea". This discipline takes a bit of work,
but it makes it much easier for code reviewers to spot bugs, and
makes the commit history a much more useful resource for developers
trying to understand why the code works the way it does, which also
helps a lot in preventing bugs.

Coherency requirements for any commit:

-   It should pass tests (so test updates needed by a change should be
    in the same commit as the original change, not a separate "fix the
    tests that were broken by the last commit" commit).
-   It should be safe to deploy individually, or comment in detail in
    the commit message as to why it isn't (maybe with a [manual] tag).
    So implementing a new API endpoint in one commit and then adding the
    security checks in a future commit should be avoided -- the security
    checks should be there from the beginning.
-   Error handling should generally be included along with the code that
    might trigger the error.
-   TODO comments should be in the commit that introduces the issue or
    functionality with further work required.

When you should be minimal:

-   Significant refactorings should be done in a separate commit from
    functional changes.
-   Moving code from one file to another should be done in a separate
    commits from functional changes or even refactoring within a file.
-   2 different refactorings should be done in different commits.
-   2 different features should be done in different commits.
-   If you find yourself writing a commit message that reads like a list
    of somewhat dissimilar things that you did, you probably should have
    just done 2 commits.

When not to be overly minimal:

-   For completely new features, you don't necessarily need to split out
    new commits for each little subfeature of the new feature. E.g. if
    you're writing a new tool from scratch, it's fine to have the
    initial tool have plenty of options/features without doing separate
    commits for each one. That said, reviewing a 2000-line giant blob of
    new code isn't fun, so please be thoughtful about submitting things
    in reviewable units.
-   Don't bother to split back end commits from front end commits, even
    though the backend can often be coherent on its own.

Other considerations:

-   Overly fine commits are easily squashed, but not vice versa, so err
    toward small commits, and the code reviewer can advise on squashing.
-   If a commit you write doesn't pass tests, you should usually fix
    that by amending the commit to fix the bug, not writing a new "fix
    tests" commit on top of it.

Zulip expects you to structure the commits in your pull requests to form
a clean history before we will merge them; it's best to write your
commits following these guidelines in the first place, but if you don't,
you can always fix your history using git rebase -i.

Never mix multiple changes together in a single commit, but it's great
to include several related changes, each in their own commit, in a
single pull request.  If you notice an issue that is only somewhat
related to what you were working on, but you feel that it's too minor
to create a dedicated pull request, feel free to append it as an
additional commit in the pull request for your main project (that
commit should have a clear explanation of the bug in its commit
message).  This way, the bug gets fixed, but this independent change
is highlighted for reviewers.  Or just create a dedicated pull request
for it.  Whatever you do, don't squash unrelated changes together in a
single commit; the reviewer will ask you to split the changes out into
their own commits.

It can take some practice to get used to writing your commits with a
clean history so that you don't spend much time doing interactive
rebases. For example, often you'll start adding a feature, and discover
you need to a refactoring partway through writing the feature. When that
happens, we recommend stashing your partial feature, do the refactoring,
commit it, and then finish implementing your feature.

## Commit Messages

First, check out
[these](https://github.com/zulip/zulip/commit/4869e1b0b2bc6d56fcf44b7d0e36ca20f45d0521)
[examples](https://github.com/zulip/zulip/commit/cd5b38f5d8bdcc1771ad794f37262a61843c56c0)
of commits with good commit messages.  There are a few mistakes we see
often that make commit messages less useful than they could be.

- The first line of commit messages should be written in the
    imperative and be kept relatively short while concisely explaining
    what the commit does.  And it should be clear about what part of
    the code is affected.  For example:

Good:
``` text
gather_subscriptions: Fix exception handling bad input.
zjsunit: Fix running stream_data and node tests individually.
Add GitLab integration.
```

Bad:

``` text
bugfix
gather_subscriptions was broken
fixing exception when given bad input
fix bug #234.
```

-   Use present-tense action verbs in your commit messages.

Bad:

``` text
gather_subscriptions: Fixing exception when given bad input.
gather_subscriptions: Fixed exception when given bad input.
```

-   Please use a complete sentence in the summary, ending with a period.
-   The rest of the commit message should be written in full prose and
    explain why and how the change was made. If the commit makes
    performance improvements, you should generally include some rough
    benchmarks showing that it actually improves the performance.
-   When you fix a GitHub issue, [mark that you've fixed the issue in
    your commit
    message](https://help.github.com/articles/closing-issues-via-commit-messages/)
    so that the issue is automatically closed when your code is merged.
    Zulip's preferred style for this is to have the final paragraph of
    the commit message read e.g. "Fixes: \#123."
-   Any paragraph content in the commit message should be line-wrapped
    to less than 76 characters per line, so that your commit message
    will be reasonably readable in git log in a normal terminal.
-   In your commit message, you should describe any manual testing you
    did in addition to running the automated tests, and any aspects of
    the commit that you think are questionable and you'd like special
    attention applied to.
