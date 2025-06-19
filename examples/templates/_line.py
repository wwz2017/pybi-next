from typing import Optional
from pybi.components.echarts import EChartsOption
from pybi.link_sql._mixin import QueryableMixin
from pybi.link_sql.sql_stem import escape_field_name
from pybi.link_sql.data_view_store import get_store

# https://echarts.apache.org/zh/option.html#series-bar
_series_options = {"label": {"show": True}}

# https://echarts.apache.org/zh/option.html#xAxis
_xAxis_options = {"axisLabel": {"rotate": 30}, "type": "category"}

_yAxis_options = {}


_extend_options = {
    "series_options": _series_options,
    "xAxis": _xAxis_options,
    "yAxis": _yAxis_options,
    "tooltip": {},
    "legend": {},
}


def make_line(
    source: QueryableMixin,
    *,
    x: str,
    y: str,
    color: Optional[str] = None,
    groupId: Optional[str] = None,
    subGroupId: Optional[str] = None,
    agg="avg",
):
    field_x = escape_field_name(x)
    field_y = escape_field_name(y)
    field_color = escape_field_name(color) if color else None

    select_exprs = [
        field_x,
        f"ROUND({agg}({field_y}),2) as {field_y}",
    ]

    group_by_exprs = [field_x]
    order_by_exprs = [f"{field_x} ASC"]

    if field_color:
        select_exprs.append(field_color)
        group_by_exprs.append(field_color)
        order_by_exprs.append(field_color)

    if groupId:
        select_exprs.append(f"{groupId} as groupId")
        group_by_exprs.append(groupId)
    if subGroupId:
        select_exprs.append(f"{subGroupId} as subGroupId")
        group_by_exprs.append(subGroupId)

    sql = f"SELECT {', '.join(select_exprs)} FROM {source} GROUP BY {', '.join(group_by_exprs)} ORDER BY {', '.join(order_by_exprs)}"

    option_fn_code = r"""(query_result, group_by_color_fn, groupId,subGroupId, x,y,color,extend_options)=>{
        const source = [query_result.columns,...query_result.values]
        const {series_options, ...others_options} = extend_options
        const dimensions = [x,y, ...(groupId? ['groupId', 'subGroupId'] : [])]
        const encode = {x,y, ...(groupId? {itemGroupId: "groupId",itemChildGroupId: "subGroupId"} : {})}
        const universalTransition = groupId ? {"enabled": true, "divideShape": "clone"} : {}
        
        const {dataset,series} = group_by_color_fn(dimensions,source,color,(color,index)=>{
            return {
                    ...series_options,
                    type: 'line',
                    name: color,
                    datasetIndex: index,
                    encode,
                    universalTransition,
            }
        })

        return {
            ...others_options,
            dataset,
            series,
        }
    }"""

    return EChartsOption(
        sql=sql,
        option_fn_code=option_fn_code,
        args=[
            get_store()._group_fn_js_handler,
            groupId,
            subGroupId,
            x,
            y,
            color,
            _extend_options,
        ],
    )
