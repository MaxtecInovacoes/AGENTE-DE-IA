$uri = "http://187.77.37.72:3000/api/webhooks"
$headers = @{
    #"Authorization" = "Basic YWRtaW46YWRtaW4="
    "Content-Type" = "application/json"
}
$body = @{
    url = "https://kindred-dolphin-410.convex.site/waha/webhook"
    events = @("message", "message.any")
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri $uri -Method Post -Headers $headers -Body $body
    Write-Output "SUCCESS: Webhook Configured"
    Write-Output $response
} catch {
    Write-Output "ERROR: $($_.Exception.Message)"
    if ($_.Exception.Response) {
        $stream = $_.Exception.Response.GetResponseStream()
        $reader = New-Object System.IO.StreamReader($stream)
        Write-Output $reader.ReadToEnd()
    }
}
