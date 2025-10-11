export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[]

export type Database = {
  // Allows to automatically instantiate createClient with right options
  // instead of createClient<Database, { PostgrestVersion: 'XX' }>(URL, KEY)
  __InternalSupabase: {
    PostgrestVersion: "12.2.3 (519615d)"
  }
  graphql_public: {
    Tables: {
      [_ in never]: never
    }
    Views: {
      [_ in never]: never
    }
    Functions: {
      graphql: {
        Args: {
          extensions?: Json
          operationName?: string
          query?: string
          variables?: Json
        }
        Returns: Json
      }
    }
    Enums: {
      [_ in never]: never
    }
    CompositeTypes: {
      [_ in never]: never
    }
  }
  public: {
    Tables: {
      brake_analysis: {
        Row: {
          abs_on_ratio: number | null
          brake_auc: number | null
          brake_distance: number | null
          brake_duration: number | null
          brake_peak: number | null
          brake_slope: number | null
          brake_start_dist: number | null
          brake_start_speed: number | null
          corner_index: number
          created_at: string | null
          decel_avg: number | null
          driver_id: string | null
          end_dist: number | null
          end_time: number | null
          id: string
          lap_id: string
          metrics: Json
          segment_name: string | null
          speed_end: number | null
          start_time: number | null
          track: string
          trail_braking_ratio: number | null
        }
        Insert: {
          abs_on_ratio?: number | null
          brake_auc?: number | null
          brake_distance?: number | null
          brake_duration?: number | null
          brake_peak?: number | null
          brake_slope?: number | null
          brake_start_dist?: number | null
          brake_start_speed?: number | null
          corner_index?: number
          created_at?: string | null
          decel_avg?: number | null
          driver_id?: string | null
          end_dist?: number | null
          end_time?: number | null
          id?: string
          lap_id: string
          metrics?: Json
          segment_name?: string | null
          speed_end?: number | null
          start_time?: number | null
          track: string
          trail_braking_ratio?: number | null
        }
        Update: {
          abs_on_ratio?: number | null
          brake_auc?: number | null
          brake_distance?: number | null
          brake_duration?: number | null
          brake_peak?: number | null
          brake_slope?: number | null
          brake_start_dist?: number | null
          brake_start_speed?: number | null
          corner_index?: number
          created_at?: string | null
          decel_avg?: number | null
          driver_id?: string | null
          end_dist?: number | null
          end_time?: number | null
          id?: string
          lap_id?: string
          metrics?: Json
          segment_name?: string | null
          speed_end?: number | null
          start_time?: number | null
          track?: string
          trail_braking_ratio?: number | null
        }
        Relationships: [
          {
            foreignKeyName: "brake_analysis_driver_id_fkey"
            columns: ["driver_id"]
            isOneToOne: false
            referencedRelation: "profiles"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "brake_analysis_lap_id_fkey"
            columns: ["lap_id"]
            isOneToOne: false
            referencedRelation: "lap_meta"
            referencedColumns: ["id"]
          },
        ]
      }
      corner_segments: {
        Row: {
          corner_index: number
          created_at: string | null
          end_dist: number
          id: string
          name: string
          start: number
          track: string
        }
        Insert: {
          corner_index: number
          created_at?: string | null
          end_dist: number
          id?: string
          name: string
          start: number
          track: string
        }
        Update: {
          corner_index?: number
          created_at?: string | null
          end_dist?: number
          id?: string
          name?: string
          start?: number
          track?: string
        }
        Relationships: []
      }
      feedback: {
        Row: {
          created_at: string | null
          email: string | null
          id: string
          message: string
        }
        Insert: {
          created_at?: string | null
          email?: string | null
          id?: string
          message: string
        }
        Update: {
          created_at?: string | null
          email?: string | null
          id?: string
          message?: string
        }
        Relationships: []
      }
      lap_controls: {
        Row: {
          brake: number | null
          distance: number | null
          gear: number | null
          id: number
          lap_id: string | null
          rpms: number | null
          speed: number | null
          steerangle: number | null
          throttle: number | null
          time: number | null
        }
        Insert: {
          brake?: number | null
          distance?: number | null
          gear?: number | null
          id?: number
          lap_id?: string | null
          rpms?: number | null
          speed?: number | null
          steerangle?: number | null
          throttle?: number | null
          time?: number | null
        }
        Update: {
          brake?: number | null
          distance?: number | null
          gear?: number | null
          id?: number
          lap_id?: string | null
          rpms?: number | null
          speed?: number | null
          steerangle?: number | null
          throttle?: number | null
          time?: number | null
        }
        Relationships: [
          {
            foreignKeyName: "lap_controls_lap_id_fkey"
            columns: ["lap_id"]
            isOneToOne: false
            referencedRelation: "lap_meta"
            referencedColumns: ["id"]
          },
        ]
      }
      lap_meta: {
        Row: {
          air_temp: number | null
          car: string | null
          created_at: string | null
          display_name: string | null
          hash: string | null
          id: string
          lap_time: number | null
          track: string | null
          track_temp: number | null
          user_id: string
          weather: string | null
        }
        Insert: {
          air_temp?: number | null
          car?: string | null
          created_at?: string | null
          display_name?: string | null
          hash?: string | null
          id?: string
          lap_time?: number | null
          track?: string | null
          track_temp?: number | null
          user_id: string
          weather?: string | null
        }
        Update: {
          air_temp?: number | null
          car?: string | null
          created_at?: string | null
          display_name?: string | null
          hash?: string | null
          id?: string
          lap_time?: number | null
          track?: string | null
          track_temp?: number | null
          user_id?: string
          weather?: string | null
        }
        Relationships: []
      }
      lap_raw: {
        Row: {
          chunk_index: number | null
          data: Json | null
          id: string
          lap_id: string | null
        }
        Insert: {
          chunk_index?: number | null
          data?: Json | null
          id?: string
          lap_id?: string | null
        }
        Update: {
          chunk_index?: number | null
          data?: Json | null
          id?: string
          lap_id?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "lap_raw_lap_id_fkey"
            columns: ["lap_id"]
            isOneToOne: false
            referencedRelation: "lap_meta"
            referencedColumns: ["id"]
          },
        ]
      }
      lap_vehicle_status: {
        Row: {
          abs: number | null
          brake_temp_lf: number | null
          brake_temp_lr: number | null
          brake_temp_rf: number | null
          brake_temp_rr: number | null
          bumpstop_force_lf: number | null
          bumpstop_force_lr: number | null
          bumpstop_force_rf: number | null
          bumpstop_force_rr: number | null
          bumpstopdn_ride_lf: number | null
          bumpstopdn_ride_lr: number | null
          bumpstopdn_ride_rf: number | null
          bumpstopdn_ride_rr: number | null
          bumpstopup_ride_lf: number | null
          bumpstopup_ride_lr: number | null
          bumpstopup_ride_rf: number | null
          bumpstopup_ride_rr: number | null
          clutch: number | null
          distance: number | null
          en_ap: number | null
          en_dy: number | null
          en_et: number | null
          en_gr: number | null
          en_tb: number | null
          en_td: number | null
          en_tl: number | null
          en_tw: number | null
          en_w: number | null
          g_lat: number | null
          g_lon: number | null
          id: number
          lap_beacon: number | null
          lap_id: string | null
          roty: number | null
          sus_travel_lf: number | null
          sus_travel_lr: number | null
          sus_travel_rf: number | null
          sus_travel_rr: number | null
          tc: number | null
          time: number | null
          tyre_press_lf: number | null
          tyre_press_lr: number | null
          tyre_press_rf: number | null
          tyre_press_rr: number | null
          tyre_tair_lf: number | null
          tyre_tair_lr: number | null
          tyre_tair_rf: number | null
          tyre_tair_rr: number | null
          wheel_speed_lf: number | null
          wheel_speed_lr: number | null
          wheel_speed_rf: number | null
          wheel_speed_rr: number | null
        }
        Insert: {
          abs?: number | null
          brake_temp_lf?: number | null
          brake_temp_lr?: number | null
          brake_temp_rf?: number | null
          brake_temp_rr?: number | null
          bumpstop_force_lf?: number | null
          bumpstop_force_lr?: number | null
          bumpstop_force_rf?: number | null
          bumpstop_force_rr?: number | null
          bumpstopdn_ride_lf?: number | null
          bumpstopdn_ride_lr?: number | null
          bumpstopdn_ride_rf?: number | null
          bumpstopdn_ride_rr?: number | null
          bumpstopup_ride_lf?: number | null
          bumpstopup_ride_lr?: number | null
          bumpstopup_ride_rf?: number | null
          bumpstopup_ride_rr?: number | null
          clutch?: number | null
          distance?: number | null
          en_ap?: number | null
          en_dy?: number | null
          en_et?: number | null
          en_gr?: number | null
          en_tb?: number | null
          en_td?: number | null
          en_tl?: number | null
          en_tw?: number | null
          en_w?: number | null
          g_lat?: number | null
          g_lon?: number | null
          id?: number
          lap_beacon?: number | null
          lap_id?: string | null
          roty?: number | null
          sus_travel_lf?: number | null
          sus_travel_lr?: number | null
          sus_travel_rf?: number | null
          sus_travel_rr?: number | null
          tc?: number | null
          time?: number | null
          tyre_press_lf?: number | null
          tyre_press_lr?: number | null
          tyre_press_rf?: number | null
          tyre_press_rr?: number | null
          tyre_tair_lf?: number | null
          tyre_tair_lr?: number | null
          tyre_tair_rf?: number | null
          tyre_tair_rr?: number | null
          wheel_speed_lf?: number | null
          wheel_speed_lr?: number | null
          wheel_speed_rf?: number | null
          wheel_speed_rr?: number | null
        }
        Update: {
          abs?: number | null
          brake_temp_lf?: number | null
          brake_temp_lr?: number | null
          brake_temp_rf?: number | null
          brake_temp_rr?: number | null
          bumpstop_force_lf?: number | null
          bumpstop_force_lr?: number | null
          bumpstop_force_rf?: number | null
          bumpstop_force_rr?: number | null
          bumpstopdn_ride_lf?: number | null
          bumpstopdn_ride_lr?: number | null
          bumpstopdn_ride_rf?: number | null
          bumpstopdn_ride_rr?: number | null
          bumpstopup_ride_lf?: number | null
          bumpstopup_ride_lr?: number | null
          bumpstopup_ride_rf?: number | null
          bumpstopup_ride_rr?: number | null
          clutch?: number | null
          distance?: number | null
          en_ap?: number | null
          en_dy?: number | null
          en_et?: number | null
          en_gr?: number | null
          en_tb?: number | null
          en_td?: number | null
          en_tl?: number | null
          en_tw?: number | null
          en_w?: number | null
          g_lat?: number | null
          g_lon?: number | null
          id?: number
          lap_beacon?: number | null
          lap_id?: string | null
          roty?: number | null
          sus_travel_lf?: number | null
          sus_travel_lr?: number | null
          sus_travel_rf?: number | null
          sus_travel_rr?: number | null
          tc?: number | null
          time?: number | null
          tyre_press_lf?: number | null
          tyre_press_lr?: number | null
          tyre_press_rf?: number | null
          tyre_press_rr?: number | null
          tyre_tair_lf?: number | null
          tyre_tair_lr?: number | null
          tyre_tair_rf?: number | null
          tyre_tair_rr?: number | null
          wheel_speed_lf?: number | null
          wheel_speed_lr?: number | null
          wheel_speed_rf?: number | null
          wheel_speed_rr?: number | null
        }
        Relationships: [
          {
            foreignKeyName: "lap_vehicle_status_lap_id_fkey"
            columns: ["lap_id"]
            isOneToOne: false
            referencedRelation: "lap_meta"
            referencedColumns: ["id"]
          },
        ]
      }
      multis: {
        Row: {
          anonymous_nickname: string | null
          anonymous_password: string | null
          author_id: string | null
          created_at: string | null
          description: string | null
          game: string
          game_track: string
          id: string
          is_open: boolean | null
          link: string | null
          multi_class: string
          multi_day: string[]
          multi_race: string | null
          multi_time: string | null
          title: string
          updated_at: string | null
          week: number | null
          year: number | null
        }
        Insert: {
          anonymous_nickname?: string | null
          anonymous_password?: string | null
          author_id?: string | null
          created_at?: string | null
          description?: string | null
          game: string
          game_track: string
          id?: string
          is_open?: boolean | null
          link?: string | null
          multi_class: string
          multi_day: string[]
          multi_race?: string | null
          multi_time?: string | null
          title: string
          updated_at?: string | null
          week?: number | null
          year?: number | null
        }
        Update: {
          anonymous_nickname?: string | null
          anonymous_password?: string | null
          author_id?: string | null
          created_at?: string | null
          description?: string | null
          game?: string
          game_track?: string
          id?: string
          is_open?: boolean | null
          link?: string | null
          multi_class?: string
          multi_day?: string[]
          multi_race?: string | null
          multi_time?: string | null
          title?: string
          updated_at?: string | null
          week?: number | null
          year?: number | null
        }
        Relationships: []
      }
      page_views: {
        Row: {
          id: string
          page_name: string
          updated_at: string | null
          view_count: number | null
        }
        Insert: {
          id?: string
          page_name: string
          updated_at?: string | null
          view_count?: number | null
        }
        Update: {
          id?: string
          page_name?: string
          updated_at?: string | null
          view_count?: number | null
        }
        Relationships: []
      }
      profiles: {
        Row: {
          agreed_at: string | null
          agreed_privacy: boolean | null
          agreed_terms: boolean | null
          cookie_consent: string | null
          created_at: string | null
          email: string | null
          has_uploaded_data: boolean | null
          id: string
          nickname: string | null
          role: string | null
        }
        Insert: {
          agreed_at?: string | null
          agreed_privacy?: boolean | null
          agreed_terms?: boolean | null
          cookie_consent?: string | null
          created_at?: string | null
          email?: string | null
          has_uploaded_data?: boolean | null
          id: string
          nickname?: string | null
          role?: string | null
        }
        Update: {
          agreed_at?: string | null
          agreed_privacy?: boolean | null
          agreed_terms?: boolean | null
          cookie_consent?: string | null
          created_at?: string | null
          email?: string | null
          has_uploaded_data?: boolean | null
          id?: string
          nickname?: string | null
          role?: string | null
        }
        Relationships: []
      }
      sector_results: {
        Row: {
          corner_index: number | null
          created_at: string | null
          id: string
          is_public: boolean | null
          lap_id: string | null
          sector_end: number
          sector_index: number
          sector_number: number | null
          sector_start: number
          sector_time: number
          track: string | null
          user_id: string | null
        }
        Insert: {
          corner_index?: number | null
          created_at?: string | null
          id?: string
          is_public?: boolean | null
          lap_id?: string | null
          sector_end: number
          sector_index: number
          sector_number?: number | null
          sector_start: number
          sector_time: number
          track?: string | null
          user_id?: string | null
        }
        Update: {
          corner_index?: number | null
          created_at?: string | null
          id?: string
          is_public?: boolean | null
          lap_id?: string | null
          sector_end?: number
          sector_index?: number
          sector_number?: number | null
          sector_start?: number
          sector_time?: number
          track?: string | null
          user_id?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "sector_results_lap_id_fkey"
            columns: ["lap_id"]
            isOneToOne: false
            referencedRelation: "lap_meta"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "sector_results_user_id_fkey"
            columns: ["user_id"]
            isOneToOne: false
            referencedRelation: "profiles"
            referencedColumns: ["id"]
          },
        ]
      }
    }
    Views: {
      brake_analysis_summary: {
        Row: {
          avg_brake_slope: number | null
          lap_id: string | null
          total_corners: number | null
        }
        Relationships: [
          {
            foreignKeyName: "brake_analysis_lap_id_fkey"
            columns: ["lap_id"]
            isOneToOne: false
            referencedRelation: "lap_meta"
            referencedColumns: ["id"]
          },
        ]
      }
    }
    Functions: {
      increment_home_views: {
        Args: Record<PropertyKey, never>
        Returns: number
      }
    }
    Enums: {
      [_ in never]: never
    }
    CompositeTypes: {
      [_ in never]: never
    }
  }
}

type DatabaseWithoutInternals = Omit<Database, "__InternalSupabase">

type DefaultSchema = DatabaseWithoutInternals[Extract<keyof Database, "public">]

export type Tables<
  DefaultSchemaTableNameOrOptions extends
    | keyof (DefaultSchema["Tables"] & DefaultSchema["Views"])
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof (DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"] &
        DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Views"])
    : never = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? (DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"] &
      DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Views"])[TableName] extends {
      Row: infer R
    }
    ? R
    : never
  : DefaultSchemaTableNameOrOptions extends keyof (DefaultSchema["Tables"] &
        DefaultSchema["Views"])
    ? (DefaultSchema["Tables"] &
        DefaultSchema["Views"])[DefaultSchemaTableNameOrOptions] extends {
        Row: infer R
      }
      ? R
      : never
    : never

export type TablesInsert<
  DefaultSchemaTableNameOrOptions extends
    | keyof DefaultSchema["Tables"]
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"]
    : never = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Insert: infer I
    }
    ? I
    : never
  : DefaultSchemaTableNameOrOptions extends keyof DefaultSchema["Tables"]
    ? DefaultSchema["Tables"][DefaultSchemaTableNameOrOptions] extends {
        Insert: infer I
      }
      ? I
      : never
    : never

export type TablesUpdate<
  DefaultSchemaTableNameOrOptions extends
    | keyof DefaultSchema["Tables"]
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"]
    : never = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Update: infer U
    }
    ? U
    : never
  : DefaultSchemaTableNameOrOptions extends keyof DefaultSchema["Tables"]
    ? DefaultSchema["Tables"][DefaultSchemaTableNameOrOptions] extends {
        Update: infer U
      }
      ? U
      : never
    : never

export type Enums<
  DefaultSchemaEnumNameOrOptions extends
    | keyof DefaultSchema["Enums"]
    | { schema: keyof DatabaseWithoutInternals },
  EnumName extends DefaultSchemaEnumNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaEnumNameOrOptions["schema"]]["Enums"]
    : never = never,
> = DefaultSchemaEnumNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaEnumNameOrOptions["schema"]]["Enums"][EnumName]
  : DefaultSchemaEnumNameOrOptions extends keyof DefaultSchema["Enums"]
    ? DefaultSchema["Enums"][DefaultSchemaEnumNameOrOptions]
    : never

export type CompositeTypes<
  PublicCompositeTypeNameOrOptions extends
    | keyof DefaultSchema["CompositeTypes"]
    | { schema: keyof DatabaseWithoutInternals },
  CompositeTypeName extends PublicCompositeTypeNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[PublicCompositeTypeNameOrOptions["schema"]]["CompositeTypes"]
    : never = never,
> = PublicCompositeTypeNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[PublicCompositeTypeNameOrOptions["schema"]]["CompositeTypes"][CompositeTypeName]
  : PublicCompositeTypeNameOrOptions extends keyof DefaultSchema["CompositeTypes"]
    ? DefaultSchema["CompositeTypes"][PublicCompositeTypeNameOrOptions]
    : never

export const Constants = {
  graphql_public: {
    Enums: {},
  },
  public: {
    Enums: {},
  },
} as const
