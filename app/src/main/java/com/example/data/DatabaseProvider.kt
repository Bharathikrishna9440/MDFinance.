package com.example.data

import android.content.Context
import java.security.SecureRandom
import android.util.Base64
import androidx.security.crypto.EncryptedSharedPreferences
import androidx.security.crypto.MasterKey

object DatabaseProvider {
    fun getDbPassword(context: Context): ByteArray {
        if (com.example.BuildConfig.DB_PASSWORD.isNotBlank() && com.example.BuildConfig.DB_PASSWORD != "PLACEHOLDER") {
            return com.example.BuildConfig.DB_PASSWORD.toByteArray(Charsets.UTF_8)
        }
        
        val masterKey = MasterKey.Builder(context)
            .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
            .build()
            
        val prefs = EncryptedSharedPreferences.create(
            context,
            "weekly_finance_secure_prefs",
            masterKey,
            EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
            EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
        )
        
        var storedKey = prefs.getString("db_key", null)
        if (storedKey == null) {
            val randomBytes = ByteArray(32)
            SecureRandom().nextBytes(randomBytes)
            storedKey = Base64.encodeToString(randomBytes, Base64.DEFAULT)
            prefs.edit().putString("db_key", storedKey).apply()
        }
        return Base64.decode(storedKey, Base64.DEFAULT)
    }

    fun getDatabase(context: Context): AppDatabase {
        val prefs = context.getSharedPreferences("weekly_finance_prefs", Context.MODE_PRIVATE)
        val isDemoMode = prefs.getBoolean("is_demo_mode", false)
        val currentRole = prefs.getString("current_role", "USER") ?: "USER"
        val isReadOnlyUser = currentRole == "USER"
        return AppDatabase.getDatabase(context, isDemoMode, isReadOnlyUser, getDbPassword(context))
    }
}
