import re

with open("app/src/main/java/com/example/ui/SystemUpdateSubPage.kt", "r") as f:
    content = f.read()

# The button code looks like:
#                 Button(
#                     onClick = {
#                         FirebaseUpdateManager.deleteDownloadedUpdate(context)
#                         FirebaseUpdateManager.checkForCloudUpdates(context, manualCheck = true)
#                     },
#                     colors = ButtonDefaults.buttonColors(containerColor = Color.Red),
#                     shape = RoundedCornerShape(8.dp),
#                     modifier = Modifier.fillMaxWidth()
#                 ) {
#                     Icon(
#                         imageVector = Icons.Default.Delete,
#                         contentDescription = "Delete",
#                         tint = Color.White,
#                         modifier = Modifier.size(18.dp)
#                     )
#                     Spacer(modifier = Modifier.width(8.dp))
#                     Text(
#                         text = translate("DELETE DOWNLOAD & RE-CHECK", language),
#                         fontWeight = FontWeight.Bold,
#                         fontSize = 13.sp,
#                         color = Color.White
#                     )
#                 }

button_pattern = re.compile(r'\s*Button\(\s*onClick = \{\s*FirebaseUpdateManager\.deleteDownloadedUpdate\(context\).*?DELETE DOWNLOAD & RE-CHECK.*?\}\s*\}\s*\}\s*', re.DOTALL)

# Find all occurrences
occurrences = [m for m in button_pattern.finditer(content)]
print(f"Found {len(occurrences)} occurrences")

if len(occurrences) == 3:
    # Keep the second one, remove first and third
    # Actually, let's just replace all with empty string, then add it precisely where we want it.
    pass

# Easiest way: remove all matches of the button.
content = button_pattern.sub('\n', content)

# Now add it back exactly under the "CHECK FOR UPDATES NOW" button
target_string = """                    Text(
                        text = translate("CHECK FOR UPDATES NOW", language),
                        fontWeight = FontWeight.Bold,
                        fontSize = 13.sp,
                        color = Color.White
                    )
                }"""

replacement = target_string + """
                
                Button(
                    onClick = {
                        FirebaseUpdateManager.deleteDownloadedUpdate(context)
                        FirebaseUpdateManager.checkForCloudUpdates(context, manualCheck = true)
                    },
                    colors = ButtonDefaults.buttonColors(containerColor = Color.Red),
                    shape = RoundedCornerShape(8.dp),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Icon(
                        imageVector = Icons.Default.Delete,
                        contentDescription = "Delete",
                        tint = Color.White,
                        modifier = Modifier.size(18.dp)
                    )
                    Spacer(modifier = Modifier.width(8.dp))
                    Text(
                        text = translate("DELETE DOWNLOAD & RE-CHECK", language),
                        fontWeight = FontWeight.Bold,
                        fontSize = 13.sp,
                        color = Color.White
                    )
                }"""

content = content.replace(target_string, replacement)

with open("app/src/main/java/com/example/ui/SystemUpdateSubPage.kt", "w") as f:
    f.write(content)

