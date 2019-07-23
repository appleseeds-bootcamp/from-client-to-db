var World = {};
World.start = function() {
    $(document).ready(function() {
        var contentHolder = $("#content");
        World.loadCountries(contentHolder, 0);
    })

};

World.loadCountries = function(contentHolder, page) {
    $.get("/list_countries/" + page, function(countries) {
        if ('error' in countries) {
            alert(countries.error);
        } else {
            var nextPage = $("<span />").attr("id", "next").text("Next");
            var prevPage = $("<span />").attr("id", "prev").text("Prev");
            nextPage.add(prevPage).addClass("clickable").click(function() {
                World.handlePagination($(this), page, contentHolder);
            });

            var paginationHolder = $("<div />").addClass("pagination-holder");
            if (page > 0) {
                paginationHolder.append(prevPage);
            }
            if (result["has_more"]) {
                paginationHolder.append(nextPage);
            }

            var countriesHolder = $("<ul>");
            for (i in countries) {
                var countryEntry = $("<li />").addClass("country-entry clickable");
                var imgSrc = "/images/flags/" + countries[i].Code2 + ".png";
                var countryFlag = $("<img />").attr("src", imgSrc);
                var countryName = $("<span />").addClass("country-name").text(countries[i].Name);
                countryEntry.append(countryFlag).append(countryName)
                countriesHolder.append(countryEntry);
                countryEntry.click(function(e) {
                    var currentCountry = $(this);
                    var currentCountryCode = currentCountry.attr("id");
                    $.get("/country/" + currentCountryCode, function(countryDetails) {
                        var msg = currentCountry.find(".country-name").text();
                        msg += " population is " + countryDetails.Population;
                        alert(msg);
                    }, "json");
                });
            }
            contentHolder.empty().append(countriesHolder);
        }
    }, "json");
};

World.handlePagination = function(btn, currentPage, contentHolder) {
    (btn.is("#next")) ? currentPage++ : currentPage--;
    World.loadCountries(contentHolder, currentPage);
}

World.start();