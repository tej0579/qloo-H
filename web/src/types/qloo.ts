export interface QlooTag {
  id?: string;
  name?: string;
  type?: string;
  weight?: number;
}

export interface QlooEntity {
  id: string;
  entity_id?: string;
  name: string;
  types: string[];
  subtype?: string;
  popularity?: number;
  affinity?: number;
  tags?: (string | QlooTag | { id?: string; name?: string })[];
  properties?: Record<string, any>;
}

export interface QlooSearchResult {
  results: QlooEntity[];
  count: number;
}
