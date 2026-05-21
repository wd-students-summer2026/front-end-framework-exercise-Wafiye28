# Professional Site Using Tailwind CSS

Welcome! In this assignment, you will create a three-page **professional or business-related web site** using the front-end framework, [Tailwind CSS](https://tailwindcss.com), together with [Alpine.js](https://alpinejs.dev) for the interactive components.

## Requirements

### Minimal requirements

Your grade will be determined by automated tests that check for the presence and behavior of the items below. Make sure each one is satisfied exactly as described.

1. **Three HTML pages.** Create `professional_site.html` plus two other `.html` pages (filenames are your choice) in the same directory. The two other pages must both be linked from the navigation bar on every page.

2. **A navigation bar on every page.** On every one of the three pages, include a `<nav>` element that contains:

   - A "brand" link with `href="professional_site.html"` (the site title or logo).
   - A link to each of the other two pages.
   - A hamburger `<button>` with an Alpine `@click` (or `x-on:click`) attribute. The button must have a Tailwind class that hides it at the `md` breakpoint or larger (for example `md:hidden`).
   - A "link group" element containing the page links, with a Tailwind class that makes it visible at the `md` breakpoint or larger (for example `md:flex`, `md:block`, or `md:!block`).
   - An ancestor element (typically the `<nav>` itself) with an `x-data` attribute holding the menu's open/closed state.

   When the browser is narrower than the `md` breakpoint, clicking the hamburger button must toggle the visibility of the link group.

3. **A responsive layout** on at least one page. At least three elements on the main page must use one of Tailwind's responsive breakpoint prefixes (`sm:`, `md:`, `lg:`, `xl:`, `2xl:`) so that some part of the layout visibly changes between small and larger screens.

4. **An Alpine.js image carousel** on at least one of the three pages, with all of the following:

   - A container element with an `x-data` attribute that declares both a list of image paths and a current-index variable.
   - An `<img>` element using Alpine's `:src` (or `x-bind:src`) binding so that the image source updates from state.
   - At least two clickable controls (`<button>` elements with `@click`) that change the current image - for example "previous" and "next".
   - At least three distinct source images, each no more than **1536 pixels** wide (Tailwind's `2xl` breakpoint).
   - Clicking "next" must change the displayed image's `src` attribute.

5. **At least three customizations** that go beyond Tailwind's defaults. Across all three pages combined, do **at least one** of the following (or any mix that totals three or more):

   - Use Tailwind's **arbitrary value** syntax at least three times (any class with square brackets, e.g. `bg-[#abcdef]`, `text-[22px]`, `w-[37px]`).
   - Add at least three CSS rules to a `css/custom.css` file linked from your pages.

### Extra credit

Up to 20% extra credit points may be awarded for extraordinary quality of the final design, as judged subjectively by the grader and professor.

## Set up the project

### Copy existing web site files

The work you do in this assignment will be published to the same directory where your current web site currently exists. To prevent you from accidentally deleting any of your existing web site files, copy all the files from your existing web site into the main project directory for this assignment. This means copying any existing HTML, CSS, images, and other files and directories so a copy exists within this project directory. Then we will be able to upload everything in this directory to the web server and replace all existing files without worry about losing anything.

### Add Tailwind CSS and Alpine.js

Unlike older front-end frameworks, Tailwind and Alpine do not require you to download any files. They are loaded straight from a Content Delivery Network (CDN) using a single `<script>` tag each.

- Open `professional_site.html` and add the following two lines to the `head` element of the page:

  ```html
  <script src="https://cdn.tailwindcss.com"></script>
  <script defer src="https://unpkg.com/alpinejs"></script>
  ```

- That's it - no files to download, no folders to create, no terminal commands. All of Tailwind's utility classes and all of Alpine's directives are now available to use anywhere in your HTML.

### Create the first HTML page

- Open the HTML document named `professional_site.html`.
- Add the two `script` tags from the previous step to its `head` element.
- Add a `<link>` element in the `head` to another CSS file that will hold any of your own custom CSS code. This custom CSS file will be named `css/custom.css`. (With Tailwind you will usually need very little custom CSS, but this is where it goes if you want to write any.)
- In the `body` of this HTML document, wrap your content in a centered container. A common pattern is:

  ```html
  <body>
    <div class="max-w-6xl mx-auto px-4">
      <!-- your page content here -->
    </div>
  </body>
  ```

### Create a custom CSS file

- Create the file `css/custom.css` - this will hold any custom CSS code you choose to write.
- Make sure it loads correctly in the browser when the page loads.

### Make sure Tailwind and Alpine are working

- Open the HTML page you made in your web browser. Confirm that:
  - Tailwind utility classes (such as `text-3xl` or `bg-blue-500`) take visible effect when you apply them.
  - An Alpine component (such as a simple `x-data="{ open: false }"` element with an `@click` toggle) responds to user interaction.
  - Your custom CSS file is loading correctly.

- If you don't know how to do this, or cannot get this to work, get help.

### Do the assignment

Now follow the requirements of the assignment for this HTML document, and repeat for the other 2 HTML documents.

## Helpful resources

- [Tailwind CSS documentation](https://tailwindcss.com/docs) - the searchable reference for every utility class.
- [Alpine.js documentation](https://alpinejs.dev) - the reference for the directives (`x-data`, `x-show`, `@click`, etc.) used to build interactive components.

## Submit your work

In order to submit this assignment, you must publish all modified files to the web and upload the code to GitHub.

### Upload the web page to a web server

Upload all files you have created to a web server. Your instructor will have given you instructions for how to do this.

Take note of the web address (URL) of your web page - this is the address that can be plugged into the address bar of any web browser for the web browser to load and display your web page.

### Update the settings.json file

Make sure your name, NYU Net ID, and the exact URL of your web site's home page are placed into the `settings.json` file in the appropriate places. Make sure the URL works when plugged into a web browser beforehand.

### Submit your work on GitHub

You are now ready to submit this assignment. You can do so directly from Visual Studio Code with the following steps, in the indicated order:

1. Switch to the Source Control view in Visual Studio Code - this view will show you a list of the files you have modified.
1. In the "`Message`" text field towards the top-left, enter a unique message to yourself about what you have changed and, while still with the text field selected, type `Command`-`Enter` on Mac OS X, or `Control`-`Enter` on Windows, to "commit" the changes you've made with this custom message. If you forget to hit `Command`-`Enter` after typing the message, you can instead click the "`...`" button above the message field and click the "`Commit all`" option in the menu that appears.
1. Now, click the "`...`" button above the message field and click the "`Push`" option in the menu that appears - this will upload your changes to your personal code repository on GitHub.

You have now submitted your completed assignment. Your changes are now posted to GitHub.com, where the instructor and graders can access it. Your `settings.json` file has information about who you are and where we can view your page on the web.

You can verify all this yourself manually by visiting your repository on GitHub.com and making sure the code displayed there is what you submitted.
