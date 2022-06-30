import { Button, CardHeader, Grid, IconButton, Input, Slider, Stack, TextField, Typography } from "@mui/material";
import React, { useCallback, useMemo } from "react";
import { useCellContext } from "../../../providers/CellProvider";
import { useReportContext } from "../../../providers/ReportProvider";
import { WidgetCellType } from "../../../types/notebooks";
import { Term } from "../../../types/terms";
import { TermInput } from "../../input/TermInput";
import DeleteIcon from '@mui/icons-material/Delete';
import AddIcon from '@mui/icons-material/Add';

interface ValueDistributionWidgetData {
  group_predicate?: Term[];
  filters?: {
    predicate?: Term[];
    object?: Term[];
  }[];
  group_count?: number;
}

const MAX_GROUP_COUNT = 101;

export const ValueDistributionWidget = (props: {}) => {
  const { report } = useReportContext();
  const { cell, cellRef, outputs, setCell } = useCellContext();
  const { data, source } = cell as WidgetCellType<ValueDistributionWidgetData>;

  const setData = useCallback((newData: Partial<ValueDistributionWidgetData>) => {
    const cell = cellRef.current as WidgetCellType<ValueDistributionWidgetData>;

    setCell({
      ...cell,
      data: { ...cell.data, ...newData }
    } as any)
  }, [])

  const onAddFilter = useCallback(() => {
    const data = (cellRef.current as any).data as ValueDistributionWidgetData;

    setData({
      filters: [ ...(data.filters || []), {} ]
    })
  }, [])

  const onUpdateFilter = useCallback((filterIndex: number, newFilter) => {
    const data = (cellRef.current as any).data as ValueDistributionWidgetData;

    setData({
      filters: [
        ...data.filters.slice(0, filterIndex),
        { ...data.filters[filterIndex], ...newFilter },
        ...data.filters.slice(filterIndex + 1)
      ]
    })
  }, [])

  const onDeleteFilter = useCallback((filterIndex: number) => {
    const data = (cellRef.current as any).data as ValueDistributionWidgetData;

    setData({
      filters: [
        ...data.filters.slice(0, filterIndex),
        ...data.filters.slice(filterIndex + 1)
      ]
    })
  }, [])

  const Filters = useMemo(() => {
    return (data?.filters ?? []).map((filter, index) => (
      <>
        <Grid item xs={2}/>
        <Grid item xs={5}>
          <TermInput
            datasetId={report?.dataset?.id}
            pos={'PREDICATE'}
            label="Filter values of"
            value={filter.predicate ?? []}
            onChange={(value) => onUpdateFilter(index, { predicate: value })}
          />
        </Grid>
        <Grid item xs={5}>
          <Stack direction="row" spacing={2}>
            <TermInput
              sx={{ flex: 1 }}
              datasetId={report?.dataset?.id}
              pos={'OBJECT'}
              label="Matching values"
              value={filter.object ?? []}
              onChange={(value) => onUpdateFilter(index, { object: value })}
            />
            <IconButton
              aria-label="delete"
              onClick={() => onDeleteFilter(index)}>
              <DeleteIcon/>
            </IconButton>
          </Stack>
        </Grid>
      </>
    ));
  }, [ data.filters ]);

  const GroupCount = useMemo(() => {
    const group_count = data?.group_count ?? 20;

    return (
      <Grid item xs={6}>
        <Typography gutterBottom>Limit number of groups</Typography>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs>
            <Slider
              aria-label="Small steps"
              defaultValue={20}
              valueLabelFormat={(value) => value != MAX_GROUP_COUNT ? value.toString() : 'Unlimited'}
              step={1}
              marks
              min={1}
              max={MAX_GROUP_COUNT}
              valueLabelDisplay="auto"
              value={group_count}
              onChange={(event, value) => setData({ group_count: value as number })}
            />
          </Grid>
          <Grid item>
            <Input
              value={group_count}
              size="small"
              onChange={(event) => setData({ group_count: parseInt(event.target.value) })}
              onBlur={(event) => setData({ group_count: parseInt(event.target.value) })}
              inputProps={{
                step: 10,
                min: 0,
                max: 100,
                type: 'number',
                'aria-labelledby': 'input-slider',
              }}
            />
          </Grid>
        </Grid>
      </Grid>
    )
  }, [ data.group_count ]);

  const Content = (
    <Grid container spacing={2}>
      <Grid item xs={12}>
        <CardHeader
          sx={{ p: 0 }}
          title="Value Distribution Query Builder"
          subheader="Plots distribution of values for a given predicate and a filter"
        />
      </Grid>
      <Grid item xs={2}>
        <TextField label="Value" value="Any" variant="filled" disabled={true}/>
      </Grid>
      <Grid item xs={10}>
        <TermInput
          datasetId={report?.dataset?.id}
          pos={'PREDICATE'}
          label="Group values of"
          value={data?.group_predicate ?? []}
          onChange={(value) => setData({ group_predicate: value })}
        />
      </Grid>
      {Filters}
      <Grid item xs={2}/>
      <Grid item xs={10}>
        <Button variant="text" startIcon={<AddIcon/>} onClick={onAddFilter}> Add filter</Button>
      </Grid>
      {GroupCount}
      <Grid item xs={6}/>
    </Grid>
  )

  return (
    <>
      {Content}
      <Typography>Value Distribution</Typography>
    </>
  )
}