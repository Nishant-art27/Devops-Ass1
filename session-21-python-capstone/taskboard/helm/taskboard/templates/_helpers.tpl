{{/*
Release "taskboard" gives "taskboard"; release "demo" gives "demo-taskboard".
*/}}
{{- define "taskboard.fullname" -}}
{{- if contains .Chart.Name .Release.Name -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s-%s" .Release.Name .Chart.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}

{{- define "taskboard.backendName" -}}{{ include "taskboard.fullname" . }}-backend{{- end -}}
{{- define "taskboard.frontendName" -}}{{ include "taskboard.fullname" . }}-frontend{{- end -}}
{{- define "taskboard.postgresName" -}}{{ include "taskboard.fullname" . }}-postgres{{- end -}}

{{- define "taskboard.labels" -}}
app.kubernetes.io/name: taskboard
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version }}
{{- end -}}
