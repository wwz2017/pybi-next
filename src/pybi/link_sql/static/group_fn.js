

/**
 * @param {any[]} dimensions 
 * @param {any[][]} source 
 * @param {string?} color 
 * @param {(color:string,index:number)=> any} series_fn 
 */
function group_by_color_fn(dimensions, source, color, series_fn) {
    const color_index = color ? source[0].indexOf(color) : null

    if (color_index === undefined || color_index === null) {
        return {
            dataset: [{ dimensions, source }],
            series: [series_fn(color, 0)],
        }
    }

    const header = source[0].filter((_, index) => index !== color_index)
    const group_map = new Map()

    source.slice(1).forEach(row => {
        const key = row[color_index]
        const value = row.filter((_, index) => index !== color_index)
        if (group_map.has(key)) {
            group_map.get(key).push(value)
        } else {
            group_map.set(key, [value])
        }
    })

    const sources = Array.from(group_map.values()).map(row => [header, ...row]);
    const colors = Array.from(group_map.keys())
    const dataset = sources.map(source => ({ dimensions, source }))
    const series = colors.map((color, index) => series_fn(color, index))

    return { dataset, series }
}