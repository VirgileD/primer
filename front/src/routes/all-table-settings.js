export const columnSettings = [{
      key: "title",
      title: "Title",
      /** @type {function(import('$lib/types').Show) : string} */
      value: s => s.title,
      sortable: true,
    },{
        key: "release_year",
        title: "Release Year",
        /** @type {function(import('$lib/types').Show) : number} */
        value: s => s.release_year,
        sortable: true,
      },{
        key: "rating",
        title: "IMdb Rating",
        /** @type {function(import('$lib/types').Show) : number} */
        value: s => s.rating,
        sortable: true,
      },{
        key: "directors",
        title: "directors",
        /** @type {function(import('$lib/types').Show) : string} */
        value: s => { console.log(s.directors); return s.directors.join(", ")},

      },{
        key: "starring",
        title: "starring",
        /** @type {function(import('$lib/types').Show) : string} */
        value: s => s.starring.join(", "),
      },
    ];