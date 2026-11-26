param(
    [Parameter(Mandatory = $true)]
    [string]$Username
)

$credential = Get-Credential -UserName $Username -Message "Enter ${Username}'s demo password"

$response = Invoke-RestMethod `
    -Method Post `
    -Uri "http://127.0.0.1:8081/realms/cater-again/protocol/openid-connect/token" `
    -ContentType "application/x-www-form-urlencoded" `
    -Body @{
        grant_type = "password"
        client_id  = "cater-again-client"
        username   = $credential.UserName
        password   = $credential.GetNetworkCredential().Password
    } `
    -ErrorAction Stop

$response.access_token | Set-Clipboard -ErrorAction Stop
Write-Host "Access token copied to clipboard."