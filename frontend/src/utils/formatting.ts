import dayjs from 'dayjs'

export const formatDateTime = (date: Date): string => {
  return dayjs(date).format('YYYY-MM-DD HH:mm:ss')
}

export const formatDuration = (date: Date): string => {
  return (dayjs(date) as any).fromNow()
}

export const formatUUIDShort = (uuid: string, length = 6): string => {
  return uuid.substring(0, length).toUpperCase()
}

export const formatBinding = (binding: any, prefixes: { [p: string]: string }): string => {
  return binding?.type === 'uri'
    ? formatIri(binding.value, prefixes || {})
    : binding.value;

}

export const formatIri = (iri: string, prefixes: Record<string, string>): string => {
  let result = iri;
  for (const [ alias, prefix ] of Object.entries(prefixes || {})) {
    if (iri.startsWith(prefix)) {
      result = `${alias}:${iri.slice(prefix.length)}`;
      break;
    }
  }
  return result;
}

export const extractIriLabel = (iri: string): string => {
  return iri.split('/').pop().split('#').pop().replaceAll(/[_-]/g, ' ');
}

