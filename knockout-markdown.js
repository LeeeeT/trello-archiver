(function (factory) {
    if (typeof require === "function" && typeof exports === "object" && typeof module === "object") {
        factory(require("knockout"), require("markdown-it"));
    } else if (typeof define === "function" && define["amd"]) {
        define(["knockout"], ["markdown-it"], factory);
    } else {
        factory(ko, markdownit);
    }
}
    (function (ko, markdown) {
        ko.markdown = markdown();

        ko.bindingHandlers.markdown = {
            update: function (element, valueAccessor, allBindingsAccessor) {
                var allBindings = allBindingsAccessor();
                var markdownBinding = allBindings.markdown;

                var markdownData = ko.unwrap(markdownBinding);
                var formattedData = ko.markdown.render(markdownData);

                formattedData = formattedData.replace(/(@\w+)/g, "<b>$1</b>");
                element.innerHTML = formattedData;
            }
        };
    }));
